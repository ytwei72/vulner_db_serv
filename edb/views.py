from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param, req_post_param, req_post_param_int, \
    req_post_param_dict
import common.config
from common.utils.general import SysUtils

from edb.exploitdb import ExploitDB
from edb.exploit_methods import ExploitMethods

import pymongo
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
    edb_id = req_post_param(request, "edb_id")
    title = req_post_param(request, "title")
    author = req_post_param(request, "author")
    type = req_post_param(request, "type")
    platform = req_post_param(request, "platform")

    # 检查id是否符合要求，包括取值范围和是否冲突（edb_id需要唯一）
    suggest_edb_id = exploit_db.get_suggest_edb_id(edb_id)
    if suggest_edb_id != edb_id:
        return app_err_p(Error.INVALID_EDB_ID, {'suggest_edb_id': suggest_edb_id})

    # with common.config.g_mongo_client.start_session(causal_consistency=True) as session:
    #     """事物必须在session下执行,with保证了session的正常关闭"""
    # with session.start_transaction():
    #     """一旦出现异常会自动调用session.abort_transaction()"""
    # 获取各字段的索引号，如果是新值，则添加一条新索引，并返回新的id号
    author_id = exploit_db.fetch_field_id('author', author)
    type_id = exploit_db.fetch_field_id('type', type)
    platform_id = exploit_db.fetch_field_id('platform', platform)

    # 组装漏洞信息，并添加
    item = {'description': [edb_id, title], 'date_published': SysUtils.get_now_time().strftime('%Y-%m-%d'),
            'verified': 0, 'port': 0,
            'author': {'id': author_id, 'name': author}, 'type': {'id': type_id, 'name': type},
            'platform': {'id': platform_id, 'platform': platform}, 'edb_id': edb_id}
    result = exploit_db.add(item)
    # 本版本不检查成功与否
    return app_ok()


def update(request):
    edb_id = req_post_param(request, "edb_id")
    title = req_post_param(request, "title")
    author = req_post_param(request, "author")
    type = req_post_param(request, "type")
    platform = req_post_param(request, "platform")

    # edb_id不存在，表示没有可以更新的漏洞信息条目
    if not exploit_db.exist_edb_id(edb_id):
        return app_err(Error.EDB_ID_NOT_FOUND)

    # 获取各字段的索引号，如果是新值，则添加一条新索引，并返回新的id号
    author_id = exploit_db.fetch_field_id('author', author)
    type_id = exploit_db.fetch_field_id('type', type)
    platform_id = exploit_db.fetch_field_id('platform', platform)

    # 组装漏洞信息，并更新
    item = {'description': [edb_id, title], 'author': {'id': author_id, 'name': author},
            'type': {'id': type_id, 'name': type}, 'platform': {'id': platform_id, 'platform': platform}}
    result = exploit_db.update(edb_id, item)
    # 本版本不检查成功与否
    return app_ok()


def delete(request):
    edb_id = req_get_param(request, "edb_id")
    if int(edb_id) < exploit_db.get_user_defined_id_base_int():
        return app_err_p(Error.NEED_USER_DEFINED_EDB_ID,
                         {'user_defined_id_base': exploit_db.get_user_defined_id_base()})

    # edb_id不存在，表示没有可以删除的漏洞信息条目
    if not exploit_db.exist_edb_id(edb_id):
        return app_err(Error.EDB_ID_NOT_FOUND)
    result = exploit_db.delete(edb_id)
    # 本版本不检查成功与否
    return app_ok()


def query_type(request):
    return app_ok_p(exploit_db.query_type())


def query_platform(request):
    return app_ok_p(exploit_db.query_platform())


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
