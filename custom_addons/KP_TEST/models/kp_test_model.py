from odoo import fields, models


class KPTestItem(models.Model):
    _name = 'kp.test.item'
    _description = 'KP Test Item'
    _order = 'name'

    name = fields.Char(required=True)
    description = fields.Text()
    is_active = fields.Boolean(default=True)
