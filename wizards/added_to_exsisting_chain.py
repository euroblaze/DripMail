from odoo import fields, models, api


# from odoo.exceptions import ValidationError
# from datetime import date

class AddToExistingMailChain(models.TransientModel):
    _name = 'add.to.existing.mail.chain'

    mailing_chain_name = fields.Many2one('mailing.chain')

    def addtoexsistingchain(self):
        tickets = self.env['mailing.mailing'].browse(self._context.get('active_ids', []))
        self.mailing_chain_name.sudo().write({'mailing_ids': [(4, i) for i in tickets.ids]})
        for i in tickets:
            i.write({'added_to_chain': True})
