# Copyright 2017-2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PosCategory(models.Model):
    _inherit = 'pos.category'

    product_count = fields.Integer(
        '# Products', compute='_compute_product_count',
        help="The number of products under this point of sale category "
        "(children categories included)")

    def _compute_product_count(self):
        pto = self.env['product.template']
        for categ in self:
            categ.product_count = pto.search_count([('pos_categ_ids', 'in', categ.id)])
