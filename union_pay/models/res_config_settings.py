# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_id = fields.Char(string=u'平台用户ID')
    api_email = fields.Char(string=u'联系邮箱')
    api_appid = fields.Char(string=u'API认证账号(AppId)')
    api_appsecret = fields.Char(string=u'API认证密钥(AppSecret)')
    api_publickey = fields.Text(string=u'RSA公钥(PublicKey)')
    api_signature = fields.Char(string=u'用户签名密钥(Signature)')
    api_testfile1 = fields.Boolean(string="是否有效")
    auto_token = fields.Boolean(string="自动获取Token")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            api_id=self.env['ir.config_parameter'].sudo().get_param('union_pay.api_id'),
            api_email=self.env['ir.config_parameter'].sudo().get_param('union_pay.api_email'),
            api_appid=self.env['ir.config_parameter'].sudo().get_param('union_pay.api_appid'),
            api_appsecret=self.env['ir.config_parameter'].sudo().get_param('union_pay.api_appsecret'),
            api_publickey=self.env['ir.config_parameter'].sudo().get_param('union_pay.api_publickey'),
            api_signature=self.env['ir.config_parameter'].sudo().get_param('union_pay.api_signature'),
            api_testfile1=self.env['ir.config_parameter'].sudo().get_param('union_pay.api_testfile1'),
            auto_token=self.env['ir.config_parameter'].sudo().get_param('union_pay.auto_token'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('union_pay.api_id', self.api_id)
        self.env['ir.config_parameter'].sudo().set_param('union_pay.api_email', self.api_email)
        self.env['ir.config_parameter'].sudo().set_param('union_pay.api_appid', self.api_appid)
        self.env['ir.config_parameter'].sudo().set_param('union_pay.api_appsecret', self.api_appsecret)
        self.env['ir.config_parameter'].sudo().set_param('union_pay.api_publickey', self.api_publickey)
        self.env['ir.config_parameter'].sudo().set_param('union_pay.api_signature', self.api_signature)
        self.env['ir.config_parameter'].sudo().set_param('union_pay.api_testfile1', self.api_testfile1)
        self.env['ir.config_parameter'].sudo().set_param('union_pay.auto_token', self.auto_token)
        data = {
            'name': '银联-定时更新token值',
            'active': True,
            'model_id': self.env['ir.model'].sudo().search([('model', '=', 'union.pay.get.token')]).id,
            'state': 'code',
            'user_id': self.env.user.id,
            'numbercall': -1,
            'interval_number': 60,
            'interval_type': 'minutes',
            'code': "env['union.pay.get.token'].get_union_pay_token()",
        }
        if self.auto_token:
            cron = self.env['ir.cron'].sudo().search([('name', '=', "银联-定时更新token值")])
            if len(cron) >= 1:
                cron.sudo().write(data)
            else:
                self.env['ir.cron'].sudo().create(data)
        else:
            cron = self.env['ir.cron'].sudo().search(
                [('code', '=', "env['union.pay.get.token'].get_union_pay_token()")])
            cron.sudo().unlink()


class UnionPayConfig(models.Model):
    _description = '系统参数列表'
    _name = 'union.pay.system.conf'

    name = fields.Char(string='名称')
    key = fields.Char(string='key值')
    value = fields.Char(string='参数值')
    state = fields.Selection(string=u'有效', selection=[('y', '是'), ('n', '否'), ], default='y')
    
