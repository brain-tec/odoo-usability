# Copyright 2016-2020 Akretion (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Print ZPL Barcode via CUPS',
    'version': '16.0.1.0.0',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': 'Glue module between product_print_zpl_barcode and base_report_to_printer',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': [
        'product_print_zpl_barcode',
        'base_report_to_printer',
        ],
    'data': [
        'wizards/product_print_zpl_barcode_view.xml',
    ],
    'installable': True,
}
