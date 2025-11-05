from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    kp_categ_type = fields.Selection(
        selection=[
            ('NIMIKE', 'NIMIKE'),
            ('MATERIAALI', 'MATERIAALI'),
        ],
        compute='_compute_kp_categ_type',
        string='Category Type',
        readonly=True,
        store=False,
    )

    @api.depends('categ_id', 'categ_id.kp_category_type')
    def _compute_kp_categ_type(self):
        for product in self:
            product.kp_categ_type = product.categ_id.kp_category_type if product.categ_id else False
