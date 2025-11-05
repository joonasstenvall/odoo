from odoo import api, models
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._check_kp_nimike_bom_rules()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._check_kp_nimike_bom_rules()
        return res

    def _check_kp_nimike_bom_rules(self):
        for bom in self:
            if not bom.product_tmpl_id:
                continue
            tmpl = bom.product_tmpl_id
            # Parent must have category type NIMIKE
            categ_type = tmpl.categ_id.sudo().kp_category_type
            if categ_type and categ_type != 'NIMIKE':
                raise ValidationError(
                    "BoM parent product must have category type 'NIMIKE'.")
            # Components must be MATERIAALI categories (when set) and not services
            for line in bom.bom_line_ids:
                comp_tmpl = line.product_id.product_tmpl_id
                if comp_tmpl.type == 'service':
                    raise ValidationError(
                        "Service products cannot be used as BoM components.")
                comp_categ_type = comp_tmpl.categ_id.sudo().kp_category_type
                if comp_categ_type and comp_categ_type != 'MATERIAALI':
                    raise ValidationError(
                        "BoM components must have category type 'MATERIAALI'.")


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._check_kp_component_rules()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._check_kp_component_rules()
        return res

    def _check_kp_component_rules(self):
        for line in self:
            comp_tmpl = line.product_id.product_tmpl_id
            if comp_tmpl.type == 'service':
                raise ValidationError(
                    "Service products cannot be used as BoM components.")
            comp_categ_type = comp_tmpl.categ_id.sudo().kp_category_type
            if comp_categ_type and comp_categ_type != 'MATERIAALI':
                raise ValidationError(
                    "BoM components must have category type 'MATERIAALI'.")
