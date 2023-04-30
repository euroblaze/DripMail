{
    'name': 'Drip Marketing Tool',
    'version': '1.0',
    'category': 'Marketing',
    'summary': 'Create and manage email chains for drip marketing campaigns',
    'author': 'Simplify-ERP™',
    'website': 'https://simplify-erp.de',
    'depends': ['mail', 'mass_mailing'],
    'data': [
        'views/mail_chain.xml',
        'views/views.xml',
        'views/menu.xml',
        'wizards/add_to_chain.xml',
        'wizards/added_to_exsisting_chain_view.xml',
    ],
    'installable': True,
    'application': False,
}
