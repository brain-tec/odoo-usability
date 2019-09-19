# -*- coding: utf-8 -*-

from odoo import models, fields


class IrModel(models.Model):
    _inherit = 'ir.model'

    message_follower = fields.Boolean(string='Follow', default=False,
                                      help=u'Check if you want create followers'
                                           u' on this model')
