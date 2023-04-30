from odoo import api, fields, models
from odoo.exceptions import UserError
# from datetime import date


class MailingMailing(models.Model):
    _inherit = 'mailing.mailing'
    _order = 'sequence asc'

    gap = fields.Integer(string='Gap (days)', default=0)
    sequence = fields.Integer(help='Used to order the mails')
    mail_chain_id = fields.Many2one('mailing.chain', string="Chain")
    added_to_chain = fields.Boolean('Added to Mail Chain', default=False, tracking=1)

    def max_sequence_mailing(self):
        self.env.cr.execute("SELECT MAX(Sequence) FROM mailing_mailing")
        max_sequence = self.env.cr.fetchall()[0][0]
        if not max_sequence:
            max_sequence = 0
        else:
            max_sequence += 1
        return max_sequence

    @api.model
    def create(self, vals):
        record = super(MailingMailing, self).create(vals)
        record.sequence = self.max_sequence_mailing()
        return record

    def unlink(self):
        for record in self:
            mailing_mailing = self.env['mailing.mailing'] \
                .search([('sequence', '>', record.sequence)])
            for mailing in mailing_mailing:
                mailing.write({'sequence': mailing.sequence - 1})
        return super(MailingMailing, self).unlink()

    def delete_from_chain(self):
        self.mail_chain_id = False
        self.added_to_chain = False


class MailingChain(models.Model):
    _name = 'mailing.chain'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Name', tracking=1, required=1)
    description = fields.Text('Description', tracking=1)
    mailing_ids = fields.One2many('mailing.mailing', 'mail_chain_id')
    active = fields.Boolean('Active', default=True)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def add_to_chain(self):
        if self.mailing_ids:
            for i in self.mailing_ids:
                i.sudo().with_delay().write({'added_to_chain': True})
        else:
            raise UserError("No Mailings to add to the chain")

    def remove_from_chain(self):
        if self.mailing_ids:
            for i in self.mailing_ids:
                i.sudo().with_delay().write({'added_to_chain': False})
        else:
            raise UserError("No Mailings to remove from the chain")

    def send_mail(self):
        if self.mailing_ids:
            for i in self.mailing_ids:
                i.sudo().with_delay().send_mail()
        else:
            raise UserError("No Mailings to send")
