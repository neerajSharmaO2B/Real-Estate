from odoo import models, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        print("+++++++++++++++++++++++ wdgwefd +++++++++++++++++++++++++++")
        res = super().sold_action()

        journal = self.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", self.env.company.id)],
            limit=1
        )

        if not journal:
            raise UserError("Please configure a Sales Journal.")

        for property in self:
            if not property.buyer_id:
                continue

            income_account = property.selling_price
            if not income_account:
                raise UserError(
                    "Please set an Income Account on the Property Type."
                )
            
            selling_price = property.selling_price or 0.0
            print(selling_price)
            invoice_vals = {
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    (0, 0, {
                        "name": f"6% commission for {property.name}",
                        "quantity": 1,
                        "price_unit": selling_price * 0.06,
                        #"account_id": income_account.id,
                    }),
                    (0, 0, {
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                        #"account_id": income_account.id,
                    }),
                ],
            }

            invoice = self.env["account.move"].create(invoice_vals)
            invoice.action_post()

        return res
