# Copyright 2015-2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    standard_price_company_currency = fields.Float(
        compute='_compute_margin', store=True, digits='Product Price',
        string='Unit Cost in Company Currency',
        help="Unit Cost in company currency in the unit of measure "
        "of the invoice line (which may be different from the unit "
        "of measure of the product).")
    standard_price_invoice_currency = fields.Float(
        compute='_compute_margin', store=True, digits='Product Price',
        string='Unit Cost in Invoice Currency',
        help="Unit Cost in invoice currency in the unit of measure "
        "of the invoice line (which may be different from the unit "
        "of measure of the product).")
    margin_invoice_currency = fields.Monetary(
        compute='_compute_margin', store=True,
        string='Margin in Invoice Currency', currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        compute='_compute_margin', store=True,
        string='Margin in Company Currency',
        currency_field='company_currency_id')
    margin_rate = fields.Float(
        string="Margin Rate", readonly=True, store=True,
        compute='_compute_margin',
        digits=(16, 2), help="Margin rate in percentage of the sale price")

    @api.depends(
        'product_id', 'product_uom_id', 'display_type', 'quantity', 'price_subtotal',
        'move_id.currency_id', 'move_id.move_type', 'move_id.company_id', 'move_id.date')
    def _compute_margin(self):
        for ml in self:
            standard_price_comp_cur = 0.0
            standard_price_inv_cur = 0.0
            margin_inv_cur = 0.0
            margin_comp_cur = 0.0
            margin_rate = 0.0
            if (
                    ml.display_type == 'product' and
                    ml.product_id and
                    ml.move_type in ('out_invoice', 'out_refund')):
                move = ml.move_id
                date = move.date
                company = move.company_id
                company_currency = company.currency_id
                move_currency = move.currency_id
                standard_price_comp_cur = ml.product_id.with_company(company.id).standard_price
                if ml.product_uom_id and ml.product_uom_id != ml.product_id.uom_id:
                    standard_price_comp_cur = ml.product_id.uom_id._compute_price(
                        standard_price_comp_cur, ml.product_uom_id)
                standard_price_inv_cur = company_currency._convert(
                    standard_price_comp_cur, move_currency, company, date)
                margin_inv_cur =\
                    ml.price_subtotal - (ml.quantity * standard_price_inv_cur)
                margin_comp_cur = move_currency._convert(
                    margin_inv_cur, company_currency, company, date)
                if ml.price_subtotal:
                    margin_rate = 100 * margin_inv_cur / ml.price_subtotal
                # for a refund, margin should be negative
                # but margin rate should stay positive
                if ml.move_type == 'out_refund':
                    margin_inv_cur *= -1
                    margin_comp_cur *= -1
            ml.standard_price_company_currency = standard_price_comp_cur
            ml.standard_price_invoice_currency = standard_price_inv_cur
            ml.margin_invoice_currency = margin_inv_cur
            ml.margin_company_currency = margin_comp_cur
            ml.margin_rate = margin_rate


class AccountMove(models.Model):
    _inherit = 'account.move'

    margin_invoice_currency = fields.Monetary(
        string='Margin in Invoice Currency',
        compute='_compute_margin', store=True,
        currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency',
        compute='_compute_margin', store=True,
        currency_field='company_currency_id')

    @api.depends(
        'move_type',
        'invoice_line_ids.margin_invoice_currency',
        'invoice_line_ids.margin_company_currency')
    def _compute_margin(self):
        rg_res = self.env['account.move.line'].read_group(
            [
                ('move_id', 'in', self.ids),
                ('display_type', '=', 'product'),
                ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
            ],
            ['move_id', 'margin_invoice_currency:sum', 'margin_company_currency:sum'],
            ['move_id'])
        mapped_data = dict([(x['move_id'][0], {
            'margin_invoice_currency': x['margin_invoice_currency'],
            'margin_company_currency': x['margin_company_currency'],
            }) for x in rg_res])
        for move in self:
            move.margin_invoice_currency = mapped_data.get(move.id, {}).get('margin_invoice_currency')
            move.margin_company_currency = mapped_data.get(move.id, {}).get('margin_company_currency')
