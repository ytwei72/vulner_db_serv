from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param, req_post_param, req_post_param_int, \
    req_post_param_dict
import common.config

from common.utils.general import SysUtils

import re

# cnvd 集合
cnvd_col = common.config.g_cnvd_col


class CnvdDB:

    def info_count(self):
        return cnvd_col.count()

    def query(self, offset, count):
        # CNVD的漏洞数据总数
        total = self.info_count()

        # 分页查询
        # result = cnvd_col.find({"number": {'$exists': True}}, {'_id': 0}).skip(page_id * page_size).limit(page_size)
        result = cnvd_col.find({}, {'_id': 0}).skip(offset).limit(count)
        item_list = list(result)
        payload = {'total': total, 'offset': offset}
        if item_list is None or len(item_list) == 0:
            payload['count'] = 0
            payload['items'] = {}
        else:
            payload['count'] = len(item_list)
            payload['items'] = item_list

        return payload

    def query_page(self, page_id, page_size):
        # CNVD的漏洞数据总数
        total = self.info_count()

        # 分页查询
        # result = cnvd_col.find({"number": {'$exists': True}}, {'_id': 0}).skip(page_id * page_size).limit(page_size)
        result = cnvd_col.find({}, {'_id': 0}).skip(page_id * page_size).limit(page_size)
        item_list = list(result)
        payload = {'total': total, 'page_id': page_id, 'page_size': page_size}
        if item_list is None or len(item_list) == 0:
            payload['count'] = 0
            payload['coll'] = {}
        else:
            payload['count'] = len(item_list)
            payload['coll'] = item_list

        return payload
