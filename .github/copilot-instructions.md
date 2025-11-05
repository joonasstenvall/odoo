# Odoo Development Guidelines

## Project Overview
This is an **Odoo 19.0** ERP codebase with custom addons. Odoo uses a modular architecture where functionality is organized into addons (modules) with standard structure.

## Critical Architecture Patterns

### Module Structure
Every addon follows this canonical structure:
```
addon_name/
├── __init__.py           # Import models/, controllers/, wizards/
├── __manifest__.py       # Module metadata, dependencies, data files
├── models/               # Python ORM models
│   ├── __init__.py
│   └── *.py
├── views/                # XML view definitions
├── security/             # Access rights (ir.model.access.csv, security.xml)
├── data/                 # Data files loaded at install
├── demo/                 # Demo data (optional)
├── static/               # JS/CSS/SCSS assets
├── controllers/          # Web controllers
├── wizard/               # Transient models for wizards
└── tests/                # Unit tests
```

### Model Inheritance Patterns

**Extend existing models** using `_inherit`:
```python
class ProductTemplate(models.Model):
    _inherit = 'product.template'  # Extends existing model
    
    custom_field = fields.Char('Custom Field')
```

**Create new models** using `_name`:
```python
class CustomModel(models.Model):
    _name = 'custom.model'
    _description = 'Custom Model Description'
```

**Delegation inheritance** using `_inherits` (one-to-one):
```python
class MailAliasMixin(models.AbstractModel):
    _name = 'mail.alias.mixin'
    _inherits = {'mail.alias': 'alias_id'}
    alias_id = fields.Many2one(required=True)
```

**Model types**:
- `models.Model` - Persistent database models
- `models.TransientModel` - Temporary wizard data (auto-cleaned)
- `models.AbstractModel` - Mixin classes (no table)

### XML View Inheritance

**Always use XPath** to modify existing views:
```xml
<record id="view_id" model="ir.ui.view">
    <field name="name">module.model.form.inherit</field>
    <field name="model">model.name</field>
    <field name="inherit_id" ref="base_module.view_id"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='field_name']" position="after">
            <field name="new_field"/>
        </xpath>
    </field>
</record>
```

**XPath positions**: `before`, `after`, `inside`, `replace`, `attributes`

### __manifest__.py Requirements

Critical keys for every custom addon:
```python
{
    'name': 'Module Display Name',
    'version': '1.0.0',
    'category': 'Manufacturing',  # See existing addons for categories
    'depends': ['base', 'product', 'mrp'],  # Module dependencies
    'data': [
        'security/ir.model.access.csv',  # ALWAYS first
        'views/*.xml',
        'data/*.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,  # True if top-level app
}
```

**Load order matters**: security → views → data → wizards

## Development Workflows

### Running Odoo (Windows)
```powershell
# Via start.bat (configured for this instance)
.\start.bat

# Manual invocation
.\venv\Scripts\python.exe odoo-bin -r odoo -w PASSWORD --addons-path="custom_addons,addons" -d DATABASE --db_port=5433

# Common flags:
# -u MODULE_NAME       # Update module
# -i MODULE_NAME       # Install module
# --dev=all           # Auto-reload on file changes
# --test-enable       # Run tests
```

### Module Installation
```python
# After creating/modifying module:
# 1. Restart Odoo with -u module_name
# 2. Or in UI: Apps → Update Apps List → Install/Upgrade
```

### Testing
Tests in `tests/` directory are auto-discovered. Use decorators:
```python
from odoo.tests import tagged, Form
from odoo.addons.mrp.tests.common import TestMrpCommon

@tagged('post_install', '-at_install')  # Run after installation
class TestMyFeature(TestMrpCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup code
    
    def test_something(self):
        # Use Form for record creation (triggers onchanges)
        with Form(self.env['model.name']) as form:
            form.field_name = value
        record = form.save()
```

Run tests: `python odoo-bin --test-enable -i module_name --stop-after-init`

## Code Style & Conventions

### Python
- Follow **PEP 8** with Odoo-specific extensions
- Use `ruff` for linting (config in `ruff.toml`)
- Import order: `from odoo import api, fields, models`
- Use `Command` for one2many/many2many operations:
  ```python
  Command.create({})  # Create new record
  Command.link(id)    # Link existing
  Command.unlink(id)  # Remove link
  Command.write(id, vals)  # Update
  ```

### Field Naming
- Standard fields: `name`, `active`, `sequence`, `company_id`
- Prefix custom fields: `kp_category_type` (see `custom_addons/kp_nimike_bom/`)
- Use snake_case for fields, CamelCase for classes

### Security Rules
**ALWAYS** create `security/ir.model.access.csv`:
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_model_user,model.user,model_model_model,base.group_user,1,1,1,0
```

### Validation Patterns
```python
@api.constrains('field1', 'field2')
def _check_constraint(self):
    for record in self:
        if record.field1 and not record.field2:
            raise ValidationError("Error message")

# Or in create/write:
def _check_kp_nimike_bom_rules(self):
    # Custom validation logic
    # See custom_addons/kp_nimike_bom/models/mrp_bom.py
```

## Custom Addons Specific

This workspace has **custom_addons/** for project-specific modules:
- `kp_nimike_bom/` - Extends MRP to enforce BoM rules based on category types
- Use `NIMIKE` category for products with BoM
- Use `MATERIAALI` category for component materials

**Pattern**: Inherit core models, add computed fields, enforce business rules in `create()`/`write()`

## Common Pitfalls

1. **Missing dependencies**: Always declare module dependencies in `depends`
2. **Incorrect load order**: Security must load before views
3. **XML syntax**: Use `ref` for external IDs: `ref="base.model_res_partner"`
4. **sudo() usage**: Use sparingly, only when bypassing access rights is necessary
5. **ORM methods**: Override `create()`, `write()`, `unlink()` for validation, not CRUD logic

## Key Files to Reference

- `odoo/models.py` - ORM base classes
- `addons/mrp/` - Manufacturing module (reference for BoM patterns)
- `custom_addons/kp_nimike_bom/` - Example custom addon structure
- `ruff.toml` - Linting rules

## Resources

- Official docs: https://www.odoo.com/documentation/19.0/
- Runbot: https://runbot.odoo.com/runbot
- Contributing: See CONTRIBUTING.md
