# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

   # If I set picking_type_id as computed field with store=True and readonly=False
   # it doesn't work when creating a PO from the smartbutton of the partner form view
   # So, for v14, I use a good old onchange !

    @api.onchange("partner_id", "company_id")
    def onchange_partner_id(self):
        super(PurchaseOrder, self).onchange_partner_id()
        if self.partner_id and self.company_id:
            partner = self.partner_id.commercial_partner_id.with_company(self.company_id.id)
            if partner.purchase_picking_type_id:
                self.picking_type_id = partner.purchase_picking_type_id
            else:
                self.picking_type_id = self._get_picking_type(self.company_id.id)
