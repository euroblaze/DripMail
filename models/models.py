from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta


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

    def action_put_in_queue(self):
        self.write({'state': 'in_queue'})
        cron = self.env.ref('mass_mailing.ir_cron_mass_mailing_queue')
        cron._trigger(
            schedule_date or fields.Datetime.now()
            for schedule_date in self.mapped('schedule_date')
        )

    @api.depends('schedule_type')
    def _compute_schedule_date(self):
        for mailing in self:
            if mailing.schedule_type == 'now' or not mailing.schedule_date:
                mailing.schedule_date = False

    @api.constrains('mail_chain_id')
    def added_to_chain_removal_logic(self):
        if self.mail_chain_id:
            print('mail chain id is: ', self.mail_chain_id)
            print('mail chain id mailing ids are: ', self.mail_chain_id.mailing_ids)
            print('mail chain id mailing ids length is: ', len(self.mail_chain_id.mailing_ids))
            print('sequence: ', len(self.mail_chain_id.mailing_ids) + 1)
            self.sequence = len(self.mail_chain_id.mailing_ids) + 1
        else:
            self.sequence = 0

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
                    # get the previous mail's schedule date
                    previous_mail_schedule_date = previous_mail.schedule_date
                    # get the current mail's schedule date
                    current_mail_schedule_date = previous_mail_schedule_date + timedelta(seconds=gap_duration)
                    # set the current mail's schedule date
                    self.schedule_date = current_mail_schedule_date
                else:
                    self.schedule_date = fields.Datetime.now() + timedelta(seconds=gap_duration)
        else:
            self.schedule_date = fields.Datetime.now()
        print('schedule date is: ', self.schedule_date)

    def delete_from_chain(self):
        self.mail_chain_id = False
        self.added_to_chain = False
        self.sequence = 0
        self.gap = 0


class MailingChain(models.Model):
    _name = 'mailing.chain'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Name', tracking=1, required=1)
    description = fields.Text('Description', tracking=1)
    mailing_ids = fields.One2many('mailing.mailing', 'mail_chain_id')
    active = fields.Boolean('Active', default=True)

    contact_list_ids = fields.Many2many('mailing.list', 'mail_chain_list_rel', string='Mailing Lists')

    @api.constrains('contact_list_ids')
    def contact_list_ids_constrains(self):
        if self.contact_list_ids:
            # assign the contact list to the mailings in the chain
            for i in self.mailing_ids:
                i.contact_list_ids = self.contact_list_ids

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
    #
    # def add_to_chain(self):
    #     if self.mailing_ids:
    #         for i in self.mailing_ids:
    #             i.sudo().write({'added_to_chain': True})
    #     else:
    #         raise UserError("No Mailings to add to the chain")
    #
    # def remove_from_chain(self):
    #     if self.mailing_ids:
    #         for i in self.mailing_ids:
    #             i.sudo().write({'added_to_chain': False})
    #     else:
    #         raise UserError("No Mailings to remove from the chain")
    #
    # def send_mail(self):
    #     if self.mailing_ids:
    #         for i in self.mailing_ids:
    #             i.sudo().send_mail()
    #     else:
    #         raise UserError("No Mailings to send")
