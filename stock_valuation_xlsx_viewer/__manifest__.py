# Copyright 2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Valuation XLSX Viewer',
    'version': '14.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Glue module between stock_viewer and stock_valuation_xlsx',
    'description': """
Stock Valuation XLSX Viewer
===========================

Allows to use the module stock_valuation_xlsx when the user is part of the Stock/Viewer group.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['stock_viewer', 'stock_valuation_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_menu.xml',
        ],
    'installable': True,
}
