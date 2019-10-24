import time
from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param, req_post_param, req_post_param_int, \
    req_post_param_dict
import common.config
from common.utils.general import SysUtils
from common.utils.strutil import StrUtils
from common.syslog import SysLog

from edb.exploitdb import ExploitDB
from edb.exploit_pocs import ExploitPocs
from edb.xls_utils import XlsUtils
from edb.edb_stat import EdbStat

import pymongo
from bson.son import SON
from django.http import HttpResponse, FileResponse
from django.utils.http import urlquote
import xlrd
import xlwt

exploit_db = ExploitDB()
edb_pocs = ExploitPocs()
edb_stat = EdbStat()


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
    SysLog.success('查询漏洞', '成功查询漏洞信息，查询到漏洞信息总数={}'.format(len(docs)))
    return app_ok_p({'total': total, 'count': len(docs), 'items': docs})


def fetch(request):
    edb_id = req_get_param(request, 'edb_id')
    if StrUtils.is_blank(edb_id):
        return app_err(Error.INVALID_REQ_PARAM)
    doc = exploit_db.fetch(edb_id)
    if doc is None:
        SysLog.fail('提取漏洞', '没有提取到漏洞信息（ID={}）'.format(edb_id))
        return app_err(Error.EDB_ID_NOT_FOUND)
    SysLog.success('提取漏洞', '成功提取漏洞信息（ID={}）'.format(edb_id))
    return app_ok_p(doc)


def filter(request):
    offset = req_get_param_int(request, 'offset')
    count = req_get_param_int(request, 'count')
    field = req_get_param(request, 'field')
    value = req_get_param(request, 'value')

    # 查找利用信息
    result_cursor = exploit_db.filter(field, value)
    if result_cursor is None:
        return app_err(Error.INVALID_REQ_PARAM)
    item_list = list(result_cursor)

    # 获取信息总数，并判断指定偏移量是否越界
    total = len(item_list)
    if total == 0 or offset >= total:
        return app_err_p(Error.NO_MORE_DATA, {'total': total, 'count': 0})

    # 读取指定位置和数量的利用信息
    if count > total - offset:
        count = total - offset
    item_list = item_list[offset: offset + count]
    SysLog.success('查询漏洞', '成功查询漏洞信息，查询到漏洞信息总数={}'.format(len(item_list)))
    return app_ok_p({'total': total, 'count': len(item_list), 'items': item_list})


def search(request):
    offset = req_get_param_int(request, 'offset')
    count = req_get_param_int(request, 'count')
    value = req_get_param(request, 'value')

    # 查找利用信息
    result_cursor = exploit_db.search(value)
    item_list = list(result_cursor)

    # 获取信息总数，并判断指定偏移量是否越界
    total = len(item_list)
    if total == 0 or offset >= total:
        return app_err_p(Error.NO_MORE_DATA, {'total': total, 'count': 0})

    # 读取指定位置和数量的利用信息
    if count > total - offset:
        count = total - offset
    item_list = item_list[offset: offset + count]
    # 为性能测试中降低CPU使用率，小段延时
    time.sleep(0.5)
    SysLog.success('搜索漏洞', '成功搜索漏洞信息，查询到漏洞信息总数={}'.format(len(item_list)))
    return app_ok_p({'total': total, 'count': len(item_list), 'items': item_list})


def add(request):
    # edb_id = req_post_param(request, "edb_id")
    title = req_post_param(request, "title")
    author = req_post_param(request, "author")
    type = req_post_param(request, "type")
    platform = req_post_param(request, "platform")

    # 获取可用的edb_id，内部检查取值范围和是否冲突（edb_id需要唯一）
    edb_id = exploit_db.get_suggest_edb_id(None)

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
            'verified': 0, 'port': 0, 'customized': 1,
            'author': {'id': author_id, 'name': author}, 'type': {'id': type_id, 'name': type},
            'platform': {'id': platform_id, 'platform': platform}, 'edb_id': edb_id}
    result = exploit_db.add(item)

    # 为性能测试中降低CPU使用率，小段延时
    time.sleep(0.5)

    # 本版本不检查成功与否
    SysLog.success('新建漏洞', '成功添加漏洞信息，漏洞ID={}'.format(edb_id))
    return app_ok_p({'edb_id': edb_id, 'customized': 1, 'date_published': item['date_published']})


def update(request):
    edb_id = req_post_param(request, "edb_id")
    title = req_post_param(request, "title")
    author = req_post_param(request, "author")
    type = req_post_param(request, "type")
    platform = req_post_param(request, "platform")

    # 只有定制的漏洞信息才能进行更新操作
    if not exploit_db.custom_edb_id(edb_id):
        SysLog.fail('更新漏洞', '更新漏洞（ID={}）失败，只有定制的漏洞信息才能进行更新操作。'.format(edb_id))
        return exploit_db.err_not_custom()

    # edb_id不存在，表示没有可以更新的漏洞信息条目
    if not exploit_db.exist_edb_id(edb_id):
        SysLog.fail('更新漏洞', '更新漏洞失败，该漏洞（ID={}）不存在。'.format(edb_id))
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
    SysLog.success('更新漏洞', '成功更新漏洞信息，漏洞ID={}'.format(edb_id))
    return app_ok()


def delete(request):
    edb_id = req_get_param(request, "edb_id")
    if not exploit_db.custom_edb_id(edb_id):
        SysLog.fail('删除漏洞', '删除漏洞（ID={}）失败，只有定制的漏洞信息才能进行删除操作。'.format(edb_id))
        return exploit_db.err_not_custom()

    # edb_id不存在，表示没有可以删除的漏洞信息条目
    if not exploit_db.exist_edb_id(edb_id):
        SysLog.fail('删除漏洞', '删除漏洞失败，该漏洞（ID={}）不存在。'.format(edb_id))
        return app_err(Error.EDB_ID_NOT_FOUND)
    result = exploit_db.delete(edb_id)

    # 本版本不检查成功与否
    SysLog.success('删除漏洞', '成功删除漏洞信息，漏洞ID={}'.format(edb_id))
    return app_ok()


def query_type(request):
    return app_ok_p(exploit_db.query_type())


def query_platform(request):
    return app_ok_p(exploit_db.query_platform())


def poc_query(request):
    offset = req_get_param_int(request, 'offset')
    count = req_get_param_int(request, 'count')

    # 获取信息总数
    total = edb_pocs.count()
    # 指定偏移量越界，则报错
    if offset >= total:
        return app_err_p(Error.NO_MORE_DATA, {'total': total, 'count': 0})

    # 读取利用方法数据
    docs = edb_pocs.query(offset, count)
    SysLog.success('查询POC', '成功查询漏洞的POC，总数={}'.format(len(docs)))
    return app_ok_p({'total': total, 'count': len(docs), 'items': docs})


def poc_fetch(request):
    edb_id = req_get_param(request, 'edb_id')
    doc = exploit_db.fetch(edb_id)
    poc = edb_pocs.fetch(edb_id)
    if doc is None:
        return app_err(Error.EDB_POC_NOT_FOUND)
    SysLog.success('提取POC', '成功提取漏洞的POC（漏洞ID={}）'.format(edb_id))
    doc['poc'] = poc
    return app_ok_p(doc)


def poc_add(request):
    edb_id = req_post_param(request, 'edb_id')
    alias = req_post_param(request, 'alias')
    content = req_post_param(request, 'content')
    # 这三个参数都是POC的基本参数，不能为空
    if StrUtils.is_blank(edb_id) or StrUtils.is_blank(alias) or StrUtils.is_blank(content):
        return app_err(Error.INVALID_REQ_PARAM)

    # 只有定制漏洞才能添加POC
    if not exploit_db.custom_edb_id(edb_id):
        SysLog.fail('添加POC', '添加POC失败（漏洞ID={}）'.format(edb_id))
        return exploit_db.err_not_custom()

    # edb_id不存在，表示没有可以添加POC的漏洞信息条目
    if not exploit_db.exist_edb_id(edb_id):
        SysLog.fail('添加POC', '添加POC失败（漏洞ID={}）'.format(edb_id))
        return app_err(Error.EDB_ID_NOT_FOUND)

    edb_pocs.add(edb_id, alias, content)
    SysLog.success('添加POC', '成功添加漏洞的POC（漏洞ID={}）'.format(edb_id))
    return app_ok()


def poc_update(request):
    edb_id = req_post_param(request, 'edb_id')
    alias = req_post_param(request, 'alias')
    content = req_post_param(request, 'content')
    # 这三个参数都是POC的基本参数，不能为空
    if StrUtils.is_blank(edb_id) or StrUtils.is_blank(alias) or StrUtils.is_blank(content):
        return app_err(Error.INVALID_REQ_PARAM)

    # 只有定制漏洞才能添加POC
    if not exploit_db.custom_edb_id(edb_id):
        SysLog.fail('更新POC', '更新POC失败（漏洞ID={}）'.format(edb_id))
        return exploit_db.err_not_custom()

    # edb_id不存在，表示没有可以添加POC的漏洞信息条目
    if not exploit_db.exist_edb_id(edb_id):
        SysLog.fail('更新POC', '更新POC失败（漏洞ID={}）'.format(edb_id))
        return app_err(Error.EDB_ID_NOT_FOUND)

    # 更新POC
    edb_pocs.update(edb_id, alias, content)
    SysLog.success('更新POC', '成功更新漏洞的POC（漏洞ID={}）'.format(edb_id))
    return app_ok()


def poc_delete(request):
    edb_id = req_get_param(request, 'edb_id')
    if StrUtils.is_blank(edb_id):
        return app_err(Error.INVALID_REQ_PARAM)

    # 删除POC
    if not edb_pocs.delete(edb_id):
        SysLog.fail('删除POC', '删除POC失败（漏洞ID={}）'.format(edb_id))
        return app_err(Error.EDB_POC_NOT_FOUND)

    SysLog.success('删除POC', '成功删除漏洞的POC（漏洞ID={}）'.format(edb_id))
    return app_ok()


def poc_search(request):
    offset = req_get_param_int(request, 'offset')
    count = req_get_param_int(request, 'count')
    value = req_get_param(request, 'value')

    # 查找利用信息
    result_cursor = exploit_db.search(value)
    item_list = list(result_cursor)

    # 获取信息总数，并判断指定偏移量是否越界
    total = len(item_list)
    if total == 0 or offset >= total:
        return app_err_p(Error.NO_MORE_DATA, {'total': total, 'count': 0})

    # 读取指定位置和数量的利用信息
    if count > total - offset:
        count = total - offset
    item_list = item_list[offset: offset + count]

    # 查询poc信息，添加到漏洞信息中
    # poc_list = []
    for item in item_list:
        poc = edb_pocs.fetch_no_content(item['edb_id'])
        item['poc'] = poc
        # poc_list.append(poc)
    SysLog.success('搜索POC', '成功搜索POC文件，总数={}'.format(len(item_list)))
    return app_ok_p({'total': total, 'count': len(item_list), 'items': item_list})


def poc_download(request):
    edb_id = req_get_param(request, 'edb_id')
    item = edb_pocs.fetch(edb_id)
    if item is None:
        return app_err(Error.EDB_POC_NOT_FOUND)

    file_name = item['aliases']
    response = HttpResponse(item['content'], content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(file_name))
    SysLog.success('下载POC', '成功下载POC文件，漏洞ID={}'.format(edb_id))
    return response


def max_id(request):
    max_id = exploit_db.max_edb_id()
    return app_ok_p({'max_id': max_id})


def export_excel(request):
    id_list_str = req_get_param(request, 'id_list')
    # ID号区间查询因为需要先在整个集合把edb_id转为整数，速度较慢，关闭不用
    # id_from = req_get_param(request, 'id_from')
    # id_to = req_get_param(request, 'id_to')

    if id_list_str is not None:
        id_list = id_list_str.split(',')
        item_list = exploit_db.fetch_some(id_list)
    # elif not StrUtils.is_blank(id_from) and not StrUtils.is_blank(id_to):
    #     item_list = exploit_db.fetch_range(id_from, id_to)
    else:
        item_list = exploit_db.query_all()

    file_name = XlsUtils.write_excel(item_list)
    xls_file = open(file_name, "rb")
    response = FileResponse(xls_file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % file_name
    SysLog.success('导出', '成功导出excel文件，漏洞ID={}'.format(id_list_str))
    return response


def stat_verified(request):
    stat = edb_stat.verified_stat()
    return app_ok_p(stat)


def stat_years(request):
    stat = edb_stat.years_stat()
    return app_ok_p(stat)


def stat_platform(request):
    stat = edb_stat.platform_stat()
    return app_ok_p(stat)


def stat_type(request):
    stat = edb_stat.type_stat()
    return app_ok_p(stat)

