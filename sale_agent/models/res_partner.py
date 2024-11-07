# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    agent = fields.Boolean()
    # agent_id is only displayed on parent partner
    # on sale.order and invoice, it uses commercial_partner_id.agent_id.id
    agent_id = fields.Many2one(
        'res.partner', domain=[('agent', '=', True)], ondelete='restrict', copy=False)
