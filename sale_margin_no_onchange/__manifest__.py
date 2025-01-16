# Copyright 2015-2025 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "Sale Margin No Onchange",
    "version": "16.0.1.0.0",
    "category": "Sales",
    "license": "AGPL-3",
    "summary": "Copy standard price on sale order line and compute margins",
    "description": """
This module copies the cost of the product on the sale order line when the sale order line is created and it computes the margin amount (in the currency of the order and in the currency of the company) and the margin rate. It also computes the total margin of the sale order (in the currency of the order and in the currency of the company).

I decided to develop this module as an alternative to the OCA sale margin modules because I wanted a small and simple module. The module *account_invoice_margin*, available in the same Github repository, does the same thing on customer invoices.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    "author": "Akretion",
    "website": "https://github.com/akretion/odoo-usability",
    "depends": ["sale"],
    "data": ["views/sale_order.xml", "views/sale_report.xml"],
    "installable": True,
}
