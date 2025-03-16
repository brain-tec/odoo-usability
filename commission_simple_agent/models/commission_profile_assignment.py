# Copyright Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CommissionProfileAssignment(models.Model):
    _inherit = "commission.profile.assignment"

    agent_id = fields.Many2one(
        'res.partner', ondelete='restrict',
        compute="_compute_agent_id", store=True, readonly=False,
        domain=[('agent', '=', True)])

    _sql_constraints = [
        (
            'company_agent_uniq',
            'unique(agent_id, company_id)',
            'This agent already has an assignment in this company.')]

    @api.model
    def _assign_type_selection(self):
        sel = super()._assign_type_selection()
        sel.append(('agent', _('Agent')))
        return sel

    @api.constrains('assign_type', 'agent_id')
    def _check_agent(self):
        for assignment in self:
            if assignment.assign_type == 'agent' and not assignment.agent_id:
                raise ValidationError(_("An agent must be selected when the assignment type is 'Agent'."))

    @api.depends('assign_type')
    def _compute_agent_id(self):
        for assign in self:
            if assign.assign_type != 'agent':
                assign.agent_id = False

    def _prepare_move_line_domain(self, date_range):
        domain = super()._prepare_move_line_domain(date_range)
        if self.assign_type == 'agent':
            domain.append(('move_id.invoice_agent_id', '=', self.agent_id.id))
        return domain

    def _get_partner(self):
        self.ensure_one()
        if self.assign_type == 'agent':
            return self.agent_id
        return super()._get_partner()
