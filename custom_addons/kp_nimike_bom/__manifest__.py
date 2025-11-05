{
    'name': 'KP NIMIKE BoM',
    'version': '1.0.0',
    'summary': 'Enable BoM for products of NIMIKE category',
    'category': 'Manufacturing',
    'license': 'LGPL-3',
    'depends': ['product', 'mrp', 'sale_mrp'],
    'data': [
        'views/product_category_views.xml',
        'views/mrp_product_views.xml',
        'views/mrp_bom_views.xml',
    ],
    'installable': True,
    'application': False,
}