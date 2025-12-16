from odoo import http
from odoo.http import request

class SaleServicePortal(http.Controller):

    @http.route('/my/orders', type='http', auth='user', website=True)
    def portal_orders(self, **kwargs):
        partner_id = request.env.user.partner_id.id
        orders = request.env['ss.sale.order'].search([('partner_id','=',partner_id)])
        return request.render('sale_service.portal_orders', {'orders': orders})