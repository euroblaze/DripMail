from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date


class Mailing(models.Model):
    _inherit = 'mailing.mailing'

    gap = fields.Integer(string='Gap (days)', default=0)
    mail_chain_id = fields.Many2one('mailing.chain', string="Chain")
    added_to_chain = fields.Boolean('Added to Mail Chain', default=False, tracking=1)

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
