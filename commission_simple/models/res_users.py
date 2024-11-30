# Copyright 2019-2024 Akretion France (https://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # TODO mon idée : déplacer ça dans une table dédiée
    # company_id oblig
    # partner_id (filtré... sur lien vers user ou agent petit difficulté)
    # profile_id
    # type agent ou user => ça donne le champ de recherche

    commission_profile_id = fields.Many2one(
        'commission.profile', string='Commission Profile',
        company_dependent=True)
