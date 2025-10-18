# Copyright 2016-2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools import misc, float_compare


class BaseUsabilityInstalled(models.AbstractModel):
    _name = "base.usability.installed"
    _description = "Base Usability Installed"


formatLang_original = misc.formatLang


def formatLang(
        env, value, digits=None, grouping=True,
        monetary=False, dp=False, currency_obj=False, int_no_digits=True):
    if (
            'base.usability.installed' in env and
            int_no_digits and
            not monetary and
            isinstance(value, float) and
            dp):
        prec = env['decimal.precision'].precision_get(dp)
        if not float_compare(value, int(value), precision_digits=prec):
            digits = 0
            dp = False
    res = formatLang_original(
        env, value, digits=digits, grouping=grouping,
        monetary=monetary, dp=dp, currency_obj=currency_obj)
    return res


misc.formatLang = formatLang
