# Copyright 2015-2026 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, Command
from odoo.exceptions import ValidationError


class ProductCategTaxMixin(models.AbstractModel):
    _name = 'product.categ.tax.mixin'
    _description = 'Common code for taxes on product categories'

    @api.onchange('categ_id')
    def onchange_categ_id(self):
        # NO sudo(), only in current company, because otherwize you get an ir.rule error
        # anyway, it is just for the user interface, because it will go later in create()
        # or write()
        if self.categ_id:
            self.taxes_id, self.supplier_taxes_id = (
                self._apply_tax_from_category(self.categ_id))

    @api.model
    def _apply_tax_from_category(self, categ):
        # I cannot use the commented line below:
        # self.taxes_id = self.categ_id.sale_tax_ids.ids
        #   because it ADDS the taxes (equivalent of (4, ID)) instead
        #   of replacing the taxes... and I want to REPLACE the taxes
        #   So I have to use the awful syntax (6, 0, [IDs])
        # values are sent to ('taxes_id' and 'supplier_taxes_id')
        return ([Command.set(categ.sale_tax_ids.ids)],
                [Command.set(categ.purchase_tax_ids.ids)])

    @api.model
    def _tax_update_vals(self, categ, vals):
        # use sudo() to get taxes from ALL companies
        vals['taxes_id'], vals['supplier_taxes_id'] = self._apply_tax_from_category(categ.sudo())
        allowed_company_ids = list(self.env['res.company']._search([]))
        # Put self.env.company at the first position of allowed_company_ids
        # because in the ORM code he takes self.env.company as allowed_company_ids[0]
        cur_company_id = self.env.company.id
        if cur_company_id in allowed_company_ids:
            allowed_company_ids.remove(cur_company_id)
            allowed_company_ids.insert(0, cur_company_id)
        return allowed_company_ids

    @api.model_create_multi
    def create(self, vals_list):
        allowed_company_ids = self.env.company.ids
        for vals in vals_list:
            if vals.get('categ_id'):
                categ = self.env['product.category'].browse(vals['categ_id'])
                allowed_company_ids = self._tax_update_vals(categ, vals)
        return super(ProductCategTaxMixin, self.with_context(allowed_company_ids=allowed_company_ids)).create(vals_list)

    def write(self, vals):
        if vals.get('categ_id'):
            categ = self.env['product.category'].browse(vals['categ_id'])
            allowed_company_ids = self._tax_update_vals(categ, vals)
            return super(ProductCategTaxMixin, self.with_context(allowed_company_ids=allowed_company_ids)).write(vals)
        elif vals.get('taxes_id') or vals.get('supplier_taxes_id'):
            for product in self:
                categ = product.categ_id
                pvals = dict(vals)
                allowed_company_ids = self._tax_update_vals(categ, pvals)
                super(ProductCategTaxMixin, product.with_context(allowed_company_ids=allowed_company_ids)).write(pvals)
            return True
        return super().write(vals)


class ProductTemplate(models.Model):
    _inherit = ['product.template', 'product.categ.tax.mixin']
    _name = 'product.template'

    @api.constrains('taxes_id', 'supplier_taxes_id', 'categ_id')
    def _check_tax_categ(self):
        for pt in self:
            if pt.categ_id:
                if pt.categ_id.sale_tax_ids.ids != pt.taxes_id.ids:
                    raise ValidationError(self.env._(
                        "The sale taxes configured on the product '%(product)s' "
                        "are not the same as the sale taxes configured "
                        "on it's related internal category '%(categ)s'.",
                        product=pt.display_name, categ=pt.categ_id.display_name))
                if (
                        pt.categ_id.purchase_tax_ids.ids !=
                        pt.supplier_taxes_id.ids):
                    raise ValidationError(self.env._(
                        "The purchase taxes configured on the product '%(product)s' "
                        "are not the same as the purchase taxes configured "
                        "on it's related internal category '%(categ)s'.",
                        product=pt.display_name, categ=pt.categ_id.display_name))


class ProductProduct(models.Model):
    _inherit = ['product.product', 'product.categ.tax.mixin']
    _name = 'product.product'


class ProductCategory(models.Model):
    _inherit = 'product.category'

    sale_tax_ids = fields.Many2many(
        'account.tax', 'product_categ_sale_tax_rel', 'categ_id', 'tax_id',
        string="Sale Taxes", domain=[('type_tax_use', '=', 'sale')])
    purchase_tax_ids = fields.Many2many(
        'account.tax', 'product_categ_purchase_tax_rel', 'categ_id', 'tax_id',
        string="Purchase Taxes", domain=[('type_tax_use', '=', 'purchase')])
