# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError


class HrTimesheetSheet(models.Model):
    _inherit = 'hr_timesheet.sheet'

    def show_lines_fullscreen(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "hr_timesheet.timesheet_action_all")
        action['domain'] = [('sheet_id', '=', self.id)]
        return action

    # Inherit native method. We don't want tons of followers by default. We just want the manager.
    def _get_subscribers(self):
        self.ensure_one()
        subscribers = self._get_informables()
        return subscribers

    def _check_can_review(self):
        if self.employee_id.user_id == self.env.user and self.employee_id.parent_id:
            raise UserError(_("You cannot approve your own timesheet!"))
        return super()._check_can_review()
