# Copyright (C) 2025 Akretion (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Stock Default Picking Type on Partner',
    'version': '16.0.1.0.0',
    'category': 'Purchases',
    'license': 'AGPL-3',
    'summary': 'Configure the default picking type for purchase orders on partners',
    'description': """
Purchase Stock Default Picking Type on Partner
==============================================

Allow to configure on partners the default picking type for purchase orders.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['purchase_stock'],
    'data': ['views/res_partner.xml'],
    'installable': True,
}
