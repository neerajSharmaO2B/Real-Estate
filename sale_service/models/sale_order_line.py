from odoo import models, fields, api

class SaleServiceOrderLine(models.Model):
    _name = 'ss.sale.order.line'
    _description = 'Sale & Service Order Line'

    order_id = fields.Many2one('ss.sale.order', string='Order', required=True, ondelete='cascade')
    product_name = fields.Char(string='Service / Product', required=True)
    quantity = fields.Integer(default=1)
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity','price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit