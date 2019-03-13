# unionPay
OdooERP12银联支付模块

# 基于odoo12开发的银联模块，主要功能为
- 设置银联平台信息（银联平台用户ID、appid）等
- 系统参数列表（银联接口地址、token值等）
- 定时刷新token值（因银联token值有效期为2小时。过期便失效，所有需要定时获取token）
- 查询银行卡信息
