from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    kp_category_type = fields.Selection(
        selection=[
            ('NIMIKE', 'NIMIKE'),  # Products that can have BoM
            ('MATERIAALI', 'MATERIAALI'),  # Material components category
        ],
        string='Category Type',
        help='Business type used to control BoM behavior:\n'
             '- NIMIKE: Product that can have a Bill of Materials.\n'
             '- MATERIAALI: Goods that can be used as components in BoMs.',
    )
