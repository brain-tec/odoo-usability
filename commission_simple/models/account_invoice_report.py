# Copyright 2018-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    commission_amount = fields.Float(readonly=True)

    @api.model
    def _select(self):
        select_str = super()._select()
        select_str += ", line.commission_amount * currency_table.rate AS commission_amount"
        return select_str
