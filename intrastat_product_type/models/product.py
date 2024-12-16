# Copyright 2016-2024 Akretion France (https://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    intrastat_type = fields.Selection([
        ('product', 'Product'),
        ('service', 'Service'),
        ],
        compute='_compute_intrastat_type',
        readonly=False, store=True, precompute=True, required=True,
        help="Type of product used for the intrastat declarations. "
        "It allows you to configure a service product as 'Consumable' "
        "to have it in pickings but configure it with "
        "Intrastat Type = 'Service' to consider it as a "
        "service for intrastat declarations.")

    @api.depends('type')
    def _compute_intrastat_type(self):
        for pt in self:
            if pt.type in ('product', 'consu'):
                intrastat_type = 'product'
            else:
                intrastat_type = 'service'
            pt.intrastat_type = intrastat_type

    @api.constrains('type', 'intrastat_type')
    def _check_intrastat_type(self):
        for pt in self:
            if pt.type != 'consu' and pt.intrastat_type != pt.type:
                raise ValidationError(_(
                    "On product '%s' which is not a consumable, "
                    "Intrastat Type must have the same value as Type.")
                    % pt.display_name)

    # inherit method from intrastat_base
    @api.constrains("intrastat_type", "is_accessory_cost")
    def _check_accessory_cost(self):
        for this in self:
            if this.is_accessory_cost and this.intrastat_type != "service":
                raise ValidationError(
                    _(
                        "The option 'Is accessory cost?' should only be "
                        "activated on 'Service' products. You have activated "
                        "this option for the product '%(product_name)s' which is "
                        "configured with type '%(product_type)s'."
                    )
                    % {
                        "product_name": this.display_name,
                        "product_type": this._fields["type"].convert_to_export(
                            this.type, this
                        ),
                    }
                )
