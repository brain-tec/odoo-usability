# -*- coding: utf-8 -*-
# Copyright 2017-2024 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    display_name = fields.Char(compute="_compute_display_name", store=True, string="Name")
    # copy=False on 'ref' is already in base_usability

    _sql_constraints = [(
        'ref_unique',
        'unique(ref)',
        'A partner already exists with this internal reference!'
        )]

    # inspired by _display_name_compute from base module
    @api.multi
    @api.depends('parent_id', 'is_company', 'name', 'ref')
    def _compute_display_name(self):
        for partner in self:
            partner.display_name = partner.with_context(show_address=False, show_address_only=False, show_email=False).name_get()[0][1]

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            # START modif of native name_get() method
            if record.ref:
                name = u"[%s] %s" % (record.ref, name)
            # END modif of native name_get() method
            if record.parent_id and not record.is_company:
                name = "%s, %s" % (record.parent_name, name)
            if context.get('show_address_only'):
                name = self._display_address(cr, uid, record, without_company=True, context=context)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if name and operator == 'ilike':
            recs = self.search([('ref', '=', name)] + args, limit=limit)
            if recs:
                rec_childs = self.search([('id', 'child_of', recs.ids)])
                return rec_childs.name_get()
        return super(ResPartner, self).name_search(name=name, args=args, operator=operator, limit=limit)
