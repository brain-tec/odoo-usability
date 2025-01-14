# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, Command


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def _prepare_move_vals(self):
        """Copy attachments from hr.expense.sheet to supplier invoice"""
        vals = super()._prepare_move_vals()
        if self.attachment_ids:
            vals['attachment_ids'] = [Command.create({'res_model': 'account.move', 'name': attach.name, 'datas': attach.datas}) for attach in self.attachment_ids]
        return vals
