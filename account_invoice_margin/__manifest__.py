# Copyright 2015-2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Invoice Margin',
    'version': '16.0.1.0.0',
    'category': 'Invoicing Management',
    'license': 'AGPL-3',
    'summary': 'Copy standard price on invoice line and compute margins',
    'description': """
This module copies the field *standard_price* of the product on the invoice line when the invoice line is created. The allows the computation of the margin of the invoice.

A new measure *Margin* is available in the Invoice Analysis.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['account'],
    'data': [
        'views/account_move.xml',
    ],
    'installable': True,
}
