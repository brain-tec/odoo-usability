# Copyright 2026 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountGroup(models.Model):
    _inherit = 'account.group'

    @api.constrains('code_prefix_start', 'code_prefix_end')
    def _constraint_prefix_overlap(self):
        return False
        for record in self:
            # Simple hack to avoid checking the constraint on record base on
            # one digit precision as native implementation is buggy
            if len(record.code_prefix_start) != 1:
                super(AccountGroup, record)._constraint_prefix_overlap()


