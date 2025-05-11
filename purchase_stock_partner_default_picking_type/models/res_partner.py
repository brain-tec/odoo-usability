# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Used only for manual POs
    purchase_picking_type_id = fields.Many2one(
        'stock.picking.type', string="Purchase Picking Type",
        company_dependent=True,
        domain="[('code', '=', 'incoming'), ('company_id', '=', current_company_id)]")
