{
    'name': 'Drip Marketing Tool',
    'version': '1.0',
    'category': 'Marketing',
    'summary': 'Create and manage email chains for drip marketing campaigns',
    'author': 'Simplify-ERP™',
    'website': 'https://simplify-erp.de',
    'depends': ['mail', 'mass_mailing', 'queue_job'],
    'data': [
        'data/scheduled_action.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/mail_chain.xml',
        'wizards/add_to_chain.xml',
        'wizards/added_to_exsisting_chain_view.xml',
    ],
    'installable': True,
    'application': False,
}