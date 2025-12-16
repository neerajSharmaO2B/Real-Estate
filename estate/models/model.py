from odoo import models,fields,api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError
from datetime import date

class CRMmodule(models.Model):
    _name="estate.property"
    _description="Real Estate Record"
    _order="id desc"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(string="Date Availability",copy=False,default=lambda self:date.today()+relativedelta(months=3))
    expected_price = fields.Float(string = "Expected Price")
    selling_price = fields.Float(string = "Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(string = "Bedrooms",default=2)
    living_area = fields.Integer(string = "Living Area")
    fascades = fields.Integer(string = "Fascades")
    garage = fields.Boolean(string = "Garage")
    garden = fields.Boolean(string = "Garden")
    garden_area = fields.Integer(string = "Garden Area")
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East'),
        ],
        string="Garden Orientation"
    )
    active = fields.Boolean(string="Active",default=False)
    state = fields.Selection(
        [
            ('new',"New"),
            ('offer_received',"Offer Received"),
            ('offer_accepted','Offer Accepted'),
            ('sold',"Sold"),
            ('cancelled',"Cancelled"),
        ],
        string = "State",
        default="new",
        copy=False,
        required=True,
    )
    
    buyer_id = fields.Many2one("res.partner",string="Buyer",readonly="1")
    salesperson_id = fields.Many2one("res.users",string="Salesperson",default = lambda self:self.env.user)

    property_type_id = fields.Many2one("estate.property.type")
    property_tag_id = fields.Many2many("estate.property.tag",string="Tags")
    
    offer_ids = fields.One2many("estate.property.offer","property_id",string="Offers")
    
    total_area = fields.Integer(string="Total Area", compute="_totalArea_")
    
    best_price = fields.Float(string="Best Price",compute="_bestPrice_")
    
    # ============================== Functions =========================================
    
    @api.depends("living_area")
    @api.depends("garden_area")
    def _totalArea_(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _bestPrice_(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0

    @api.onchange("garden")
    def _onchange_garden_(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation='north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    # ================================ Buttons =========================================
    def cancel_action(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be cancelled.")
            record.state = 'cancelled'
        return True
    
    def sold_action(self):
        print("+++++++++++++++++++++++ Action sold +++++++++++++++++++++++++++++++++")
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled Selling price cannot be higher than expected  property cannot be sold.")
            record.state = 'sold'
        return True
    
    # ==================================== Constraints =================================================

    @api.constrains("expected_price")
    def _check_expected_price_(self):
        for price in self:
            if price.expected_price < 0 :
                raise ValidationError("Price must be higher than 0 and cannot be negative.")
            
    @api.constrains("selling_price","expected_price")
    def _check_selling_price_(self):
        for price in self:
            if price.selling_price :
                check_price = price.expected_price * 0.90
                if price.selling_price < check_price:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
            
    #==================================== Inheritance ==================================================

    @api.ondelete(at_uninstall=False)
    def _check_on_delete(self):
        for record in self:
            if record.state not in ['new','cancelled']:
                raise UserError("You can only delete properties in state 'New' or 'Cancelled'.")