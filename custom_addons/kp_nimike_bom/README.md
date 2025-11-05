# KP NIMIKE BoM

Enables Bill of Materials functionality for products with category type `NIMIKE`.

## Features

- Adds `Category Type` field to product categories with values:
  - `NIMIKE` - Products that can have a Bill of Materials
  - `MATERIAALI` - Products that can be used as BoM components
- Shows BoM smart button on products whose category type is `NIMIKE`
- Restricts BoM components to products with category type `MATERIAALI`
- Validates that BoM parents have category type `NIMIKE`
- Prevents services from being used as BoM components

## Usage

1. Install the module from Apps
2. Configure product categories:
   - Go to Inventory > Configuration > Product Categories
   - Set `Category Type = NIMIKE` for product categories that should have BoMs
   - Set `Category Type = MATERIAALI` for component categories
3. On products with NIMIKE category:
   - The "Bill of Materials" smart button will be visible
   - Click to create and manage BoMs
4. When adding BoM components:
   - Only products with MATERIAALI category type can be selected
   - Services are blocked from being components

## Dependencies

- product
- mrp
- sale_mrp
