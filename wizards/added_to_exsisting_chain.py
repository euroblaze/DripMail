from odoo import fields, models


class AddToExistingMailChain(models.TransientModel):
    _name = 'add.to.existing.mail.chain'

    mailing_chain_name = fields.Many2one('mailing.chain', domain=[('active', '=', True)])

    def addtoexsistingchain(self):
        mails = self.env['mailing.mailing'].browse(self._context.get('active_ids', []))
        self.mailing_chain_name.sudo().write({'mailing_ids': [(4, i) for i in mails.ids]})
        for i in mails:
            i.write({'added_to_chain': True, 'contact_list_ids': [(6, 0, self.mailing_chain_name.contact_list_ids.ids)],
                     'mailing_model_id': self.env.ref('mass_mailing.model_mailing_list').id})
