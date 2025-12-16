from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order="sequence,name"

    name = fields.Char(required=True)
    sequence = fields.Integer('sequence',default=10)

    property_ids = fields.One2many(
        "estate.property",     
        "property_type_id",
        string="Properties",
        onDelete = "set null",
    )
    

    _sql_constraints = [
        ('unique_property_type_name', 'unique(name)', 'Property type name must be unique!')
    ]
