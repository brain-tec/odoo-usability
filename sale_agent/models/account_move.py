# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_agent_id = fields.Many2one(
        'res.partner', domain=[('agent', '=', True)], string="Agent",
        ondelete='restrict', tracking=True,
        compute='_compute_invoice_agent_id', store=True, readonly=False, precompute=True)

    @api.depends('partner_id', 'move_type')
    def _compute_invoice_agent_id(self):
        for move in self:
            if move.is_sale_document() and move.partner_id:
                move.invoice_agent_id = move.partner_id.commercial_partner_id.agent_id.id or False
            else:
                move.invoice_agent_id = False
