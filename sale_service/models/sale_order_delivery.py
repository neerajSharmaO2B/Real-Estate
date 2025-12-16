from odoo import models, fields

class SaleServiceOrder(models.Model):
    _inherit = 'ss.sale.order'

    delivery_status = fields.Selection([
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ], default='pending', string="Delivery Status")
