from odoo import api, fields, models, tools

class DripMarketingChain(models.Model):
    _name = 'drip.marketing.chain'
    _description = 'Drip Marketing Chain'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    mailing_list_id = fields.Many2one('mailing.list', string='Mailing List')

class DripMarketingEmail(models.Model):
    _name = 'drip.marketing.email'
    _description = 'Drip Marketing Email'

    chain_id = fields.Many2one('drip.marketing.chain', string='Chain', required=True)
    subject = fields.Char(string='Subject', required=True)
    content = fields.Html(string='Content', required=True)
    gap_duration = fields.Integer(string='Gap Duration (in hours)', required=True)

    @api.model
    def process_emails(self):
        # Get the current time
        now = fields.Datetime.now()

        # Find all the mailing list contacts
        contacts = self.env['mailing.contact'].search([])

        for contact in contacts:
            # Find the associated chain for the contact's mailing list
            chain = self.env['drip.marketing.chain'].search([('mailing_list_id', '=', contact.list_id.id)], limit=1)

            if chain:
                # Find the emails that need to be sent to the contact based on the Gap interval
                emails_to_send = self.search([
                    ('chain_id', '=', chain.id),
                    ('gap_duration', '<=', tools.datetime.timedelta(hours=now - contact.create_date).total_seconds()
            ])

            for email in emails_to_send:
                # Check if the email has already been sent to the contact
                existing_mail = self.env['mail.mail'].search([
                    ('recipient_ids', 'in', [contact.id]),
                    ('subject', '=', email.subject)
                ])

                # Send the email if it hasn't been sent yet
                if not existing_mail:
                    self.env['mail.mail'].create({
                        'subject': email.subject,
                        'body_html': email.content,
                        'email_to': contact.email,
                        'recipient_ids': [(4, contact.id)],
                        'mailing_id': chain.mailing_list_id.mailing_id.id
                    }).send()
