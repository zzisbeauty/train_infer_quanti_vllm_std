# coding=utf-8

import sys, os
import json, requests, random
sys.path.append(os.getcwd())

# from all_develop.toolsfunc import *

# ai kai 任务队列数据库
# host = 'rw.hwaurora.rdsdb.com'
# port = 3306
# user = 'ai-service'
# passwd = 'Bz2F93Qc4gxsDgc'
# db = 'gkai'

# giikin 客服数据
host = 'rm-j6c3m7yn8z24fg4n10o.mysql.rds.aliyuncs.com'
port = 3306
user = 'gcrm'
passwd = 'VuAtBvfsvq4y5'
db = 'gcrm'

# 直接使用
# conn = pymysql.connect(host=host, port=port, user=user, db=db, password=passwd, charset='utf8')
# cursor = conn.cursor()
# 使用 toolsfun.py 中的数据库加载方法
# conn, cursor = mysqlConnect(host, port, db, user, passwd)


# # 读取 DW 数据库
# from odps import ODPS
# from odps import options

# # ACCESS_ID = 'LTAI5tMyE1vafa2H giikin VavDqxNG'
# # ACCESS_KEY = 'KDbuJmvkkc4aznKCrDQk4 giikin EqEtBMyBB'
# ACCESS_ID = 'LTAI5tMyE1vafa2HVav giikin DqxNG'
# ACCESS_KEY = 'KDbuJmvkk giikin c4aznKCrDQk4EqEtBMyBB'

# DEFAULT_PROJECT = 'cda'
# END_POINT = 'http://service.cn-shenzhen.maxcompute.aliyun.com/api'
# o = ODPS(ACCESS_ID, ACCESS_KEY, DEFAULT_PROJECT, endpoint=END_POINT)
# options.tunnel.use_instance_tunnel = True
# options.tunnel.limit_instance_tunnel = False  # 关闭limit限制，读取全部数据

# sql = """ select * from giikin_aliyun.tb_dwd_pro_gk_sale_campaign_df where pt = '20231115' limit 10000; """
# sql = """ select sale_id,compaign_id,optimizer,platform as 平台, adtype,tag from giikin_aliyun.tb_dwd_pro_gk_sale_campaign_df where pt = '20231115' limit 10; """
# sql = """ select spend_date, befrom, chooser_id,designer_id, opt_id, campaign_id, line_code, currency_id, ad_spend as RMB, product_id as pid, product_name as pname, category_id as cid, category_lvl1_name as 1c, category_lvl2_name as 2c,category_lvl3_name as 3c, sale_id as sid , sale_name sname,  tag,  crt_time as acttime, impressions, reach as 触及人次, clicks,  add_cart as 加购, checkout as 结算, add_pay_info as 支付INFO,  purchase as 购买, conversions as T购买 from giikin_aliyun.tb_dwd_fin_ad_spend_df where pt > '20231110' and pt <= '20231115' """
# with o.execute_sql(sql).open_reader(tunnel=True) as reader:
#      all_top_apt = reader.to_pandas()


# def getLangIDPre(source): #     # 效果也很垃圾
#     try:
#         pdLangsUrl = 'https://idc-ai.giikin.com/language/category'
#         rs = requests.post(pdLangsUrl, json={'userLanguage': source})
#         langResCode = eval(rs.text)['data'][0]['lang']
#         return langResCode
#     except:
#         return 'CN'


# def getLangIDPre(source): #     # Giikin 预测语种，但是该模型并不准确
#     try:
#         pdLangsUrl = 'https://idc-ai.giikin.com/language/category'
#         rs = requests.post(pdLangsUrl, json={'userLanguage': source})
#         langResCode = eval(rs.text)['data'][0]['lang']
#         return langResCode
#     except:
#         return ''


# def giikinTransAPI(source, sourceLanguage='JP', targetLanguage='CN'): #     # 机翻 API to do trans，  效果很垃圾
#     sourceClean = [clean(source[0])]
#     data = {
#         "origin": sourceClean,
#         "targetLanguage": targetLanguage,
#         "sourceLanguage": sourceLanguage,
#         "source": "convsTransTask",
#         "timestamp": time.time()
#     }
#     giikinTransAPI = 'https://idc-ai.giikin.com/text/translate_zh/pre'
#     response = requests.post(url=giikinTransAPI, json=data).text
#     response = response.encode('utf-8', errors='ignore').decode()
#     response = json.dumps(response)
#     response = eval(json.loads(response))['data'][0]
#     return response

from hashlib import sha1


def giikinSpiderTrans(source, platform, sourceLanguage, targetLanguage, sign, stdm, taskName):
    # 爬虫翻译
    url = "https://material.giikin.com/material/trans/batchTransV2"
    data = {
        'origin': json.dumps(source, ensure_ascii=False),  # 这个过程是将原始的待翻译列表序列化成字符串
        'transTool': platform,
        'sourceLanguage': sourceLanguage,  # 例如 JP
        'targetLanguage': targetLanguage,  # 例如 CN
        'source': taskName,
        'timestamp': stdm,
        'sign': sign,
        'is_spider': '1',
        'only_spider': '1'
    }
    res = requests.post(url, data=data).text
    res = eval(res).get('data').get('text')
    return res


def make_sha1_spider_trans(s, encoding='utf-8'):
    return sha1(s.encode(encoding)).hexdigest()


# # 调用方法
# timestm = str(int(time.time()))  # 时间戳
# spiderTransSecret = 'q2maomxpuw1lak4onwiz5tcxcvu/4tskfo4f+njmlpy='  # 固定值
# taskName = 'convDataTask'
# sign = taskName + timestm + spiderTransSecret
# sign = make_sha1_spider_trans(sign, encoding='utf-8')
# convList = ["halo", "hello", "good", "bad", "okok", "gogogo"]  # 就是一个列表
# sourceLangIDJX = "JP"
# targetLangIDJX = "CN"
# platform = 'google'
# transedConv = giikinSpiderTrans(source=convList, platform=platform, sourceLanguage=sourceLangIDJX, targetLanguage=targetLangIDJX, sign=sign, stdm=timestm, taskName=taskName)

#  ======================================================= GPT API
import time
from hashlib import sha1
# from zuntrackfiles.apis import app_secret
app_secret = 'rKLEZpkoGBX2zqkO7j8m02QOHU52e8Mq'


def make_sha1(s, encoding='utf-8'):
    return sha1(s.encode(encoding)).hexdigest()


def make_sign(timestamp, app_secret):
    # app_secret = 'rKLEZpkoGBX2zqk giikin O7j8m02QOHU52e8Mq'   # giikin 接口校验的 key
    s = "{}{}".format(timestamp, app_secret)
    token = make_sha1(s, encoding='utf-8')
    return timestamp, token


def get_chat(message, model):
    """
    gpt: gpt-3.5-turbo-16k
    gpt-4o
    ERNIE-Bot-turbo 免费
    baidu: ERNIE-Bot-turbo
    anthropic.claude-3-haiku-20240307-v1:0   小杯
    anthropic.claude-3-sonnet-20240229-v1:0  中杯
    :param message:  [{"role": "user", "content": message}]
    :param model:
    :return:
    """
    t = time.time()
    _t, _sign = make_sign(str(t), app_secret)
    url = f"https://chatgpt.giikin.com/v1/chat/conversationV4?t={_t}&sign={_sign}"
    # message format : message=[{"role": "user", "content": message}]
    payload = json.dumps({"messages": message, "model_engine": model, "source": '对话标注'})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    response = response.json()
    return response
    # print(response)

# 调用测试
# message = [{"role":"user", "content":"请介绍一下你自己"}]
# res = get_chat(message, 'gpt-4o')
# a = 1
