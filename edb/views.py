from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param, req_post_param, req_post_param_int, \
    req_post_param_dict
import common.config
from common.utils.general import SysUtils

from edb.exploitdb import ExploitDB
from edb.exploit_methods import ExploitMethods

from bson.son import SON

exploit_db = ExploitDB()
edb_methods = ExploitMethods()


def query(request):
    offset = req_get_param_int(request, 'offset')
    count = req_get_param_int(request, 'count')

    # 获取信息总数
    total = exploit_db.info_count()
    # 指定偏移量越界，则报错
    if offset >= total:
        return app_err_p(Error.NO_MORE_DATA, {'total': total, 'count': 0})

    # 读取利用信息
    docs = exploit_db.query(offset, count)
    return app_ok_p({'total': total, 'count': len(docs), 'items': docs})


def search(request):
    offset = req_get_param_int(request, 'offset')
    count = req_get_param_int(request, 'count')
    field = req_get_param(request, 'field')
    value = req_get_param(request, 'value')

    # 查找利用信息
    result_cursor = exploit_db.search(field, value)
    item_list = list(result_cursor)

    # 获取信息总数，并判断指定偏移量是否越界
    total = len(item_list)
    if total == 0 or offset >= total:
        return app_err_p(Error.NO_MORE_DATA, {'total': total, 'count': 0})

    # 读取指定位置和数量的利用信息
    if count > total - offset:
        count = total - offset
    item_list = item_list[offset: offset + count]
    return app_ok_p({'total': total, 'count': len(item_list), 'items': item_list})


def add(request):
    return


def update(request):
    return


def delete(request):
    return


def methods_query(request):
    offset = req_get_param_int(request, 'offset')
    count = req_get_param_int(request, 'count')

    # 获取信息总数
    total = edb_methods.count()
    # 指定偏移量越界，则报错
    if offset >= total:
        return app_err_p(Error.NO_MORE_DATA, {'total': total, 'count': 0})

    # 读取利用方法数据
    docs = edb_methods.query(offset, count)
    return app_ok_p({'total': total, 'count': len(docs), 'items': docs})


def methods_fetch(request):
    edb_id = req_get_param(request, 'edb_id')
    item = edb_methods.fetch(edb_id)
    if item is None:
        return app_err(Error.EDB_METHOD_NOT_FOUND)
    return app_ok_p(item)
