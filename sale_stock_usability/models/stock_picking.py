# Copyright 2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError
import logging
logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _report_delivery_prices(self):
        self.ensure_one()
        assert self.state == 'done'
        if not self.partner_id:
            raise UserError(_("Partner is not set on picking %s.") % self.display_name)
        weight_uom_categ_id = self.env.ref('uom.product_uom_categ_kgm').id
        kg_uom = self.env.ref('uom.product_uom_kgm')
        partner_pricelist = self.partner_id.property_product_pricelist
        currency = self.sale_id.currency_id or partner_pricelist.currency_id
        total_amount = 0.0
        total_weight_kg = 0.0
        lines = []
        for line in self.move_line_ids:
            move = line.move_id
            uom = line.product_uom_id
            if uom.category_id.id == weight_uom_categ_id:
                weight_kg_subtotal = uom._compute_quantity(line.qty_done, kg_uom)
            else:
                qty_product_uom = uom._compute_quantity(line.qty_done, line.product_id.uom_id)
                weight_kg_subtotal = qty_product_uom * line.product_id.weight
            if (
                    move.sale_line_id and
                    move.sale_line_id.product_id == line.product_id and
                    move.sale_line_id.product_uom_qty > 0 and
                    move.sale_line_id.product_uom == uom):
                price_unit = currency.round(
                    line.move_id.sale_line_id.price_subtotal / move.sale_line_id.product_uom_qty)
                logger.info(
                    'For move line %s, got price %s from sale order line',
                    line.display_name, price_unit)
            else:
                # TODO remove tax if tax included
                price_unit = partner_pricelist._get_product_price(
                    line.product_id, line.qty_done, uom=uom,
                    date=fields.Date.to_date(self.date_done))
                price_unit = currency.round(price_unit)
                # Only for very special case where picking is linked to sale order but this line
                # is from linked to sale order line, and the partner pricelist is NOT in the same
                # currency as the sale order pricelist. Should very rarely happen.
                if currency != partner_pricelist.currency_id:
                    raise UserError(_(
                        "The pricelist of the related sale order is in currency "
                        "%(sale_pricelist_currency)s whereas the pricelist "
                        "%(partner_pricelist_name)s of partner %(partner)s "
                        "is in currency %(partner_pricelist_currency)s.",
                        sale_pricelist_currency=self.sale_id.currency_id.name,
                        partner_pricelist_name=partner_pricelist.name,
                        partner=self.partner_id.display_name,
                        partner_pricelist_currency=partner_pricelist.currency_id.name))
                logger.info(
                    'For move line %s, got price %s from partner pricelist %s',
                    line.display_name, price_unit, partner_pricelist.display_name)
            price_subtotal = currency.round(price_unit * line.qty_done)
            total_amount += price_subtotal
            lines.append({
                'line': line,
                'qty': line.qty_done,
                'uom': uom,
                'product': line.product_id,
                'weight_kg_subtotal': weight_kg_subtotal,
                'price_unit': price_unit,
                'price_subtotal': price_subtotal,
                'lot': line.lot_id and line.lot_id.display_name or (line.lot_name or ''),
                })
        res = {
            'lines': lines,
            'currency': currency,
            'total_amount': currency.round(total_amount),
            'total_weight_kg': total_weight_kg,
            }
        return res
