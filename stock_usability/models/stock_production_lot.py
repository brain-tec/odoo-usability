# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    name = fields.Char(tracking=True)
    product_id = fields.Many2one(tracking=True)
    ref = fields.Char(tracking=True)
