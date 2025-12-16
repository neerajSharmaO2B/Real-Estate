from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Estate Property Offer"
    _order="price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ('accept','Accepted'),
            ('refuse','Refused'),
            ('pending','Pending'),
        ],
        copy = False,
        default="pending",
    )
    partner_id = fields.Many2one("res.partner",required=True)
    property_id = fields.Many2one('estate.property',required=True,store=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_computeDateDeadline_",inverse="_inverseDateDeadline_")

    # ========================================= Function =======================================

    @api.depends("validity", "create_date")
    def _computeDateDeadline_(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = base_date + relativedelta(days=offer.validity)

    def _inverseDateDeadline_(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            delta = offer.date_deadline-base_date
            offer.validity = delta.days

    # ======================================== Buttons ==========================================
    
    def action_accept(self):
        for record in self:
            if record.status == "refuse":
                raise UserError("A refused offer cannot be accepted.")
            record.status = "accept"

            record.property_id.write({
            'buyer_id': record.partner_id.id,
            'selling_price': record.price
        })
    
    def action_refuse(self):
        for record in self:
            if record.status == "accept":
                raise UserError("A accepted offer cannot be refused.")
            record.status = "refuse"

    # ======================================= Constraints =========================================
    @api.constrains("price")
    def _check_price_(self):
        for price in self:
            if price.price < 0 :
                raise ValidationError("Offer Price must be positive.")


    # ======================================= Inheritance ==========================================
    @api.model
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]

        final_records = self.env['estate.property.offer']

        for vals in vals_list:

            property_rec = self.env['estate.property'].browse(vals.get('property_id'))

            if property_rec.offer_ids:
                max_offer = max(property_rec.offer_ids.mapped('price'))
                if vals['price'] < max_offer:
                    raise UserError("You cannot create an offer lower than an existing offer.")

            property_rec.state = 'offer_received'

            offer = super(EstatePropertyOffer, self).create(vals)

            final_records |= offer

        return final_records

