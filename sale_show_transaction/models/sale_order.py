# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    main_provider_id = fields.Many2one(
        'payment.provider',
        'Online payment mode',
        compute="_compute_main_provider",
        store=True)

    @api.depends("transaction_ids.state")
    def _compute_main_provider(self):
        for record in self:
            if len(record.transaction_ids.provider_id) > 1:
                for state in ["done", "authorized", "pending", "draft", "cancel", "error"]:
                    transaction = record.transaction_ids.filtered(lambda s: s.state == state)
                    if len(transaction.provider_id) > 1:
                        transaction.sorted("amount")
                    if transaction:
                        record.main_provider_id = transaction[0].provider_id
                        break
            else:
                record.main_provider_id = record.transaction_ids.provider_id

