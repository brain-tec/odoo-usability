# Copyright 2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'

    name = fields.Char(tracking=True)
    ref = fields.Char(tracking=True)
    product_id = fields.Many2one(tracking=True)
    company_id = fields.Many2one(tracking=True)
