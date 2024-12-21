# Copyright 2024 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Default Report Without Paiement",
    "summary": "Account Default Report Without Paiement",
    "version": "14.0.1.0.0",
    "category":  "reports",
    "website":  "https://github.com/OCA/account",
    "author":  "Akretion, Odoo Community Association (OCA)", 
    "license": "AGPL-3",
    "maintainers":["Kev-Roche"],
    "application": False,
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "data/data.xml",
    ],
}
