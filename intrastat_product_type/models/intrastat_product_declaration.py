# Copyright 2016-2024 Akretion France (https://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models


class IntrastatProductDeclaration(models.Model):
    _inherit = 'intrastat.product.declaration'

    def _is_product(self, invoice_line):
        if (
                invoice_line.product_id and
                invoice_line.product_id.intrastat_type == 'product'):
            return True
        else:
            return False
