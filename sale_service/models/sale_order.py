from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleServiceOrder(models.Model):
    _name = 'ss.sale.order'
    _description = 'Sale & Service Order'

    name = fields.Char(default='New', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)

    order_line_ids = fields.One2many('ss.sale.order.line','order_id', string='Order Lines')
    amount_total = fields.Float(string='Total Amount', compute='_compute_amount_total', store=True)

    state = fields.Selection([
        ('draft','Draft'),
        ('confirm','Confirmed'),
        ('done','Done'),
        ('cancel','Cancelled')
    ], default='draft')

    @api.depends('order_line_ids.subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(order.order_line_ids.mapped('subtotal'))

    @api.constrains('order_line_ids')
    def _check_order_lines(self):
        for order in self:
            if not order.order_line_ids:
                raise ValidationError('You must add at least one order line.')

    def action_confirm(self):
        self.write({'state':'confirm'})

    def action_done(self):
        self.write({'state':'done'})

    def action_cancel(self):
        self.write({'state':'cancel'})

    def action_create_invoice(self):
        self.ensure_one()
        invoice = self.env['account.move'].sudo().create({
            'move_type':'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_line_ids': [(0,0,{
                'name': line.product_name,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
            }) for line in self.order_line_ids]
        })
        return invoice