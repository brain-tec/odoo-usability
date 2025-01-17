# Copyright 2018-2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    margin = fields.Float(string='Margin', readonly=True)

    @api.model
    def _select(self):
        select_str = super()._select()
        select_str += ", line.margin_company_currency * currency_table.rate AS margin"
        return select_str
