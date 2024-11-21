# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agent_id = fields.Many2one(
        'res.partner', domain=[('agent', '=', True)],
        ondelete='restrict', tracking=True,
        compute='_compute_agent_id', store=True, readonly=False, precompute=True)

    @api.depends('partner_id')
    def _compute_agent_id(self):
        for order in self:
            if order.partner_id:
                order.agent_id = order.partner_id.commercial_partner_id.agent_id.id or False
            else:
                order.agent_id = False

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        vals['invoice_agent_id'] = self.agent_id.id or False
        return vals
