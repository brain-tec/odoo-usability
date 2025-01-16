# Copyright 2018-2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    margin = fields.Float(string='Margin', readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        margin_sum = f"""
        CASE WHEN l.product_id IS NOT NULL THEN SUM(l.margin_sale_currency
            / {self._case_value_or_one('s.currency_rate')}
            * {self._case_value_or_one('currency_table.rate')}
            ) ELSE 0
        END
        """
        res["margin"] = margin_sum
        return res
