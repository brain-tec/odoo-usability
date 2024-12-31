# Copyright 2016-2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tracking = fields.Selection(tracking=True)
    sale_delay = fields.Float(tracking=True)

    def action_view_stock_move(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock_usability_akretion.stock_move_list_first_action")
        action['domain'] = [('product_id.product_tmpl_id', 'in', self.ids)]
        action['context'] = {'search_default_done': True}
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_view_stock_move(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock_usability_akretion.stock_move_list_first_action")
        action['domain'] = [('product_id', 'in', self.ids)]
        action['context'] = {'search_default_done': True}
        return action
