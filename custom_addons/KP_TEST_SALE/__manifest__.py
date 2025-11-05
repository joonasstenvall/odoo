{
    'name': 'KP Test - Sales Integration',
    'author': 'Your Company',
    'version': '1.0.0',
    'summary': 'Use KP Test Items on Sales Order Lines',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['sale', 'KP_TEST'],
    'data': [
        'data/product_data.xml',
        'views/sale_views.xml',
    ],
    'installable': True,
    'application': False,
}
