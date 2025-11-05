from odoo import api, fields, models


class KPBomLine(models.Model):
    _name = 'kp.product.bom.line'
    _description = 'KP Product BoM Line'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product',
        required=True,
        ondelete='cascade',
        index=True,
    )
    kp_item_id = fields.Many2one(
        'kp.test.item',
        string='KP Item',
        required=True,
        domain=[('is_active', '=', True)],
    )
    quantity = fields.Float(default=1.0)
    note = fields.Char()


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    kp_bom_line_ids = fields.One2many(
        'kp.product.bom.line',
        'product_tmpl_id',
        string='KP BoM Lines',
        copy=True,
    )

    kp_bom_count = fields.Integer(
        string='BoM Items',
        compute='_compute_kp_bom_count',
        store=False,
    )

    @api.depends('kp_bom_line_ids')
    def _compute_kp_bom_count(self):
        for tmpl in self:
            tmpl.kp_bom_count = len(tmpl.kp_bom_line_ids)
