# -*- coding: utf-8 -*-
{
    'name': "银联支付",
    'summary': """银联支付模块""",
    'description': """ 银联支付模块 """,
    'author': "SuXueFeng",
    'website': "https://www.sxfblog.com",
    'category': 'pay',
    'version': '1.0',
    'depends': ['base', 'base_setup'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'security/union_pay_security.xml',
        'data/system_conf.xml',
        'views/menu.xml',
        'views/res_config_settings_views.xml',
        'views/bank_card_info.xml',
    ],
    'qweb': [
        'static/xml/*.xml'
    ]

}
