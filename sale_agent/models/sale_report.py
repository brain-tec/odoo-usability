# Copyright 2024-2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    agent_id = fields.Many2one("res.partner", readonly=True)

    def _select_additional_fields(self, fields):
        res = super()._select_additional_fields(fields)
        res["agent_id"] = ", s.agent_id"
        return res
