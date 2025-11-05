{
    'name': 'KP Bill of Materials',
    'version': '1.0.0',
    'summary': 'Lightweight BoM on Product using KP Test Items',
    'category': 'Product',
    'license': 'LGPL-3',
    'depends': ['product', 'KP_TEST'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_bom_views.xml',
    ],
    'installable': True,
    'application': False,
}
