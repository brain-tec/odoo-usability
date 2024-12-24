# Copyright 2022-2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    # native field, just change string (origin string is "Identify Customer")
    split_transactions = fields.Boolean(
        string="Split Transactions",
        help="Splits the journal entries for each transaction. It could slow down the closing process.",
        )
    # new field
    identify_customer = fields.Boolean(
        compute='_compute_identify_customer', store=True, readonly=False, precompute=True)

    @api.constrains('split_transactions', 'identify_customer')
    def _check_split_transactions_identify_customer(self):
        for method in self:
            if method.identify_customer and not method.split_transactions:
                raise ValidationError(_(
                    "On payment method '%s' the option 'Identify Customer' "
                    "is enabled, so the option 'Split Transactions' must "
                    "be enabled too.") % method.display_name)

    @api.depends('split_transactions')
    def _compute_identify_customer(self):
        for method in self:
            if not method.split_transactions and method.identify_customer:
                method.identify_customer = False
