from odoo import fields, models, api
from odoo.exceptions import ValidationError
# from datetime import date


class AddToMailingChain(models.TransientModel):
    _name = 'add.to.chain'

    chain_id = fields.Many2one('mailing.chain')

    mail_chain_name = fields.Char('Chain Name')

    def addtomailchain(self):
        tickets = self.env['mailing.mailing'].browse(self._context.get('active_ids', []))

        if set(tickets.mapped('added_to_chain')) != {False}:
            raise ValidationError("Selected Mails already been linked to Chain")

        else:

            mini_batch = self.env['mailing.chain'].create({'mailing_ids': tickets.ids,
                                                           'name': self.mail_chain_name})
            if self.mail_chain_name:
                mini_batch.sudo().write({'name': self.mail_chain_name})

            for i in tickets:
                i.write({'added_to_chain': True})
