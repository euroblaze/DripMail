from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class MailingMailing(models.Model):
    _inherit = 'mailing.mailing'
    _order = 'sequence asc'

    gap = fields.Integer(string='Gap (days)', default=0,
                         help='Gap between this mail and the previous mail in the chain', tracking=1)
    sequence = fields.Integer('Sequence', help='Used to order the mails')
    mail_chain_id = fields.Many2one('mailing.chain', string="Chain")
    added_to_chain = fields.Boolean('Added to Mail Chain', default=False, tracking=1)
    gap_schedule_date = fields.Datetime(string='Scheduled for', related='schedule_date', store=True, copy=True)
    schedule_date = fields.Datetime(string='Scheduled for', tracking=True, readonly=True,
                                    states={'draft': [('readonly', False)], 'in_queue': [('readonly', False)]},
                                    compute='_compute_schedule_date', store=True, copy=True)

    @api.model
    def _process_mass_mailing_queue_job_tasks(self):
        for mass_mailing in self:
            if mass_mailing.schedule_date < fields.Datetime.now() or not mass_mailing.schedule_date:
                user = mass_mailing.write_uid or self.env.user
                mass_mailing = mass_mailing.with_context(**user.with_user(user).context_get())
                if len(mass_mailing._get_remaining_recipients()) > 0:
                    mass_mailing.state = 'sending'
                    mass_mailing.action_send_mail()
                else:
                    mass_mailing.write({
                        'state': 'done',
                        'sent_date': fields.Datetime.now(),
                        # send the KPI mail only if it's the first sending
                        'kpi_mail_required': not mass_mailing.sent_date,
                    })

        mailings = self.env['mailing.mailing'].search([
            ('kpi_mail_required', '=', True),
            ('state', '=', 'done'),
            ('sent_date', '<=', fields.Datetime.now() - relativedelta(days=1)),
            ('sent_date', '>=', fields.Datetime.now() - relativedelta(days=5)),
        ])
        if mailings:
            mailings._action_send_statistics()

    @api.depends('schedule_type')
    def _compute_schedule_date(self):
        for mailing in self:
            if mailing.schedule_type == 'now' or not mailing.schedule_date:
                mailing.schedule_date = False

    @api.constrains('mail_chain_id')
    def added_to_chain_sequence_logic(self):
        for order in self.mapped('mail_chain_id'):
            sequence_number = 1
            for lines in order.mailing_ids:
                if lines.mail_chain_id:
                    lines.sequence = sequence_number
                    lines.gap = sequence_number - 1
                    sequence_number += 1

    @api.constrains('gap')
    def gap_logic(self):
        if self.gap < 0:
            raise UserError('Gap cannot be negative')
        elif self.gap > 0 and self.sequence > 1:
            chain_sorted_mails = self.mail_chain_id.mailing_ids.sorted(key='sequence', reverse=False)
            if chain_sorted_mails:
                # gap duration in days is the time between the current mail and the previous mail in the chain
                gap_duration = self.gap * 24 * 60 * 60
                # get the previous mail in the chain
                previous_mail = chain_sorted_mails.filtered(lambda l: l.sequence == self.sequence - 1)
                if previous_mail:
                    previous_mail_schedule_date = previous_mail.schedule_date
                    current_mail_schedule_date = previous_mail_schedule_date + timedelta(seconds=gap_duration)
                    self.schedule_date = current_mail_schedule_date
                else:
                    self.schedule_date = fields.Datetime.now() + timedelta(seconds=gap_duration)
        else:
            self.schedule_date = fields.Datetime.now()

    def delete_from_chain(self):
        self.mail_chain_id = False
        self.added_to_chain = False
        self.sequence = 0
        self.gap = 0

    def open_mail_from_chain(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Open Mail'),
            'res_model': 'mailing.mailing',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
            'views': [[False, 'form']]
        }


class MailingChain(models.Model):
    _name = 'mailing.chain'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Name', tracking=1, required=1)
    description = fields.Text('Description', tracking=1)
    mailing_ids = fields.One2many('mailing.mailing', 'mail_chain_id')
    active = fields.Boolean('Active', default=True)
    contact_list_ids = fields.Many2many('mailing.list', 'mail_chain_list_rel', string='Mailing Lists', required=True,
                                        tracking=1)

    @api.constrains('contact_list_ids')
    def contact_list_ids_constrains(self):
        if self.contact_list_ids:
            for i in self.mailing_ids:
                i.write({'contact_list_ids': [(6, 0, self.contact_list_ids.ids)],
                         'mailing_model_id': self.env.ref('mass_mailing.model_mailing_list').id})

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def send_mails_job_queue(self):
        for chain in self.search([]):
            if chain.mailing_ids:
                for i in chain.mailing_ids:
                    i.sudo().with_delay()._process_mass_mailing_queue_job_tasks()

    def func_update_chain_mails(self):
        if self.mailing_ids:
            for i in self.mailing_ids:
                if i.gap == 0:
                    i.write({'schedule_date': fields.Datetime.now()})
                elif i.gap > 0 and i.sequence >= 1:
                    chain_sorted_mails = i.mail_chain_id.mailing_ids.sorted(key='sequence', reverse=False)
                    if chain_sorted_mails:
                        gap_duration = i.gap * 24 * 60 * 60
                        previous_mail = chain_sorted_mails.filtered(lambda l: l.sequence == i.sequence - 1)
                        if previous_mail:
                            previous_mail_schedule_date = previous_mail.schedule_date
                            current_mail_schedule_date = previous_mail_schedule_date + timedelta(
                                seconds=gap_duration)
                            i.schedule_date = current_mail_schedule_date
                        else:
                            i.schedule_date = fields.Datetime.now() + timedelta(seconds=gap_duration)

    def update_chain_mails(self):
        for chain in self.search([]):
            chain.sudo().with_delay(priority=0).func_update_chain_mails()
