from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    kp_item_id = fields.Many2one('kp.test.item', string='KP Item', domain=[('is_active', '=', True)])

    @api.onchange('kp_item_id')
    def _onchange_kp_item_id(self):
        for line in self:
            if line.kp_item_id:
                # Use a generic service product to carry the sale values
                template = self.env.ref('KP_TEST_SALE.product_kp_generic_template', raise_if_not_found=False)
                product = template.product_variant_id if template else False
                if product:
                    line.product_id = product
                # Set the line's description and keep price as-is (or set to 0.0)
                name = line.kp_item_id.name
                if line.kp_item_id.description:
                    name = f"{name}\n{line.kp_item_id.description}"
                line.name = name
                # Optionally set price to 0.0; adjust if you later add pricing on KP items
                # line.price_unit = 0.0
