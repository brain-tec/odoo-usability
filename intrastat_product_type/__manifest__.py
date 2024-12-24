# Copyright 2016-2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Intrastat Product Type',
    'version': '16.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Adds a special field Intrastat Type on Products',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['intrastat_product', 'l10n_fr_intrastat_service'],
    'data': ['views/product.xml'],
    'installable': False,
}
