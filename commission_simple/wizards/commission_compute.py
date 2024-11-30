# Copyright 2019-2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
import logging
logger = logging.getLogger(__name__)


class CommissionCompute(models.TransientModel):
    _name = 'commission.compute'
    _description = 'Compute Commissions'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    date_range_type_id = fields.Many2one(related='company_id.commission_date_range_type_id')
    date_range_id = fields.Many2one(
        'date.range', required=True, string='Period',
        compute='_compute_date_range_id', store=True, precompute=True, readonly=False,
        domain="[('type_id', '=', date_range_type_id)]")
    date_start = fields.Date(related='date_range_id.date_start')
    date_end = fields.Date(related='date_range_id.date_end')

    @api.depends('company_id')
    def _compute_date_range_id(self):
        for wiz in self:
            date_range_id = False
            company = wiz.company_id
            if company and company.commission_date_range_type_id:
                type_id = company.commission_date_range_type_id.id
                last_commission_result = self.env['commission.result'].search([
                    ('company_id', '=', company.id),
                    ], order='date_end desc', limit=1)
                limit_date = last_commission_result and last_commission_result.date_end or (fields.Date.context_today(self) + relativedelta(months=-2, day=31))
                date_range = self.env['date.range'].search([
                    ('company_id', 'in', (company.id, False)),
                    ('type_id', '=', type_id),
                    ('date_start', '>', limit_date)
                    ], order='date_start', limit=1)
                date_range_id = date_range and date_range.id or False
            wiz.date_range_id = date_range_id

    def run(self):
        self.ensure_one()
        creso = self.env['commission.result']
        date_range = self.date_range_id
        existing_commissions = creso.search([
            ('date_range_id', '=', date_range.id),
            ('company_id', '=', self.company_id.id),
            ])
        if existing_commissions:
            raise UserError(_(
                'Commissions already exist for %(period)s in company %(company)s.',
                period=date_range.display_name, company=self.company_id.display_name))
        com_result_ids = self._core_compute()
        if not com_result_ids:
            raise UserError(_('No commissions generated.'))
        action = self.env['ir.actions.actions']._for_xml_id(
            'commission_simple.commission_result_action')
        action.update({
            'views': False,
            'domain': f"[('id', 'in', {com_result_ids})]",
            })
        return action

    def _core_compute(self):
        rules = self.env['commission.rule'].load_all_rules()
        com_result_ids = []
        assignments = self.env['commission.profile.assignment'].search([('company_id', '=', self.company_id.id)])
        for assignment in assignments:
            com_result = assignment._generate_commission_result(self.date_range_id, rules)
            if com_result:
                com_result_ids.append(com_result.id)
            else:
                logger.info("No commission for %s", assignment._get_partner().display_name)
        return com_result_ids
