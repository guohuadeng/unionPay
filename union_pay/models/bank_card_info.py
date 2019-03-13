# -*- coding: utf-8 -*-
import time
import json
import logging
import requests
import hashlib
from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class BankCardInfo(models.TransientModel):
    _description = '查询银行卡信息'
    _name = 'union.pay.search.bank.card.info'

    @api.model
    def search_bank_card_info(self, card_no):
        """查询银行卡信息
        :param card_no :银行卡号
        """
        card_no = card_no.replace(' ', '')
        logging.info('>>>需要查询的银行卡号为：{}'.format(card_no))
        token = self.env['union.pay.system.conf'].search([('key', '=', 'token')]).value
        api_signature = self.env['ir.config_parameter'].sudo().get_param('union_pay.api_signature')
        cardinfo_url = self.env['union.pay.system.conf'].search([('key', '=', 'cardinfo_url')]).value
        data = {'cardNo': card_no}
        time_str = int(round(time.time() * 1000))
        sha256_str = "{}{}{}".format(api_signature, json.dumps(data), time_str)
        # SHA-256算法加密
        sha256 = hashlib.sha256()
        sha256.update(sha256_str.encode('utf-8'))
        # url参数
        cardinfo_url = "{}?token={}&sign={}&ts={}".format(cardinfo_url, token, sha256.hexdigest(), time_str)
        headers = {'Content-Type': 'application/json'}
        result = requests.post(url=cardinfo_url, headers=headers, data=json.dumps(data), timeout=15)
        logging.info(result.text)
        # 解析结果
        try:
            result = json.loads(result.text)
            if result.get('respCd') != '0000':
                raise UserError("银联返回信息:{}".format(result.get('respMsg')))
            return result.get('data')
        except KeyError as e:
            raise UserError(u"KeyError异常错误：{}".format(e.message))
        except requests.exceptions.Timeout:
            raise UserError(u'请求超时！')
        except TypeError as e:
            raise UserError(u"TypeError系统错误！返回信息：{}".format(e.message))


class GetUnionPayToken(models.TransientModel):
    _description = '获取银联token值'
    _name = 'union.pay.get.token'

    @api.model
    def get_union_pay_token(self):
        """获取银联token值的方法函数
        获取token值需要用户用户唯一凭证（appid）和用户唯一凭证密钥（AppSecret）
        """
        api_appid = self.env['ir.config_parameter'].sudo().get_param('union_pay.api_appid')
        api_appsecret = self.env['ir.config_parameter'].sudo().get_param('union_pay.api_appsecret')
        if not api_appid and not api_appsecret:
            logging.info("银联设置项中的用户唯一凭证和用户唯一凭证密钥不能为空！")
            return False
        token_url = self.env['union.pay.system.conf'].search([('key', '=', 'token_url')]).value
        if not token_url:
            logging.info('获取Token值URL记录不存在')
            return False
        data = {'app_id': api_appid, 'app_secret': api_appsecret}
        # 发送数据
        result = requests.get(url=token_url, params=data, timeout=10)
        result = json.loads(result.text)
        logging.info(result)
        if result.get('respCd') == '0000':
            token = self.env['union.pay.system.conf'].search([('key', '=', 'token')])
            if token:
                token.write({
                    'value': result.get('token')
                })
        else:
            logging.info("获取银联Token失败！请检查网络是否通畅或检查日志输出")
