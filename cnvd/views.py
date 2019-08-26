from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param
from bson.son import SON
import pymongo

mongo_client = pymongo.MongoClient("mongodb://admin:123456@192.168.182.88:27017/")
# cnvd 数据库
cnvd_db = mongo_client["cnvd_share"]
# cnvd 集合
cnvd_col = cnvd_db["cnvd_share"]


def index(request):
    return app_ok_p("Hello, you're at the CNVD index.")


def retrieve(request):
    return app_err_p(Error.INTERNAL_EXCEPT, "Hello, world. You're at the CNVD index.")


def fetch(request):
    # CNVD的漏洞数据总数
    total = cnvd_col.count()

    # 分页查询
    page_id = req_get_param_int(request, 'page_id')
    page_size = req_get_param_int(request, 'page_size')
    # result = cnvd_col.find({"number": {'$exists': True}}, {'_id': 0}).skip(page_id * page_size).limit(page_size)
    result = cnvd_col.find({}, {'_id': 0}).skip(page_id * page_size).limit(page_size)
    if result.count() == 0:
        payload = {'total': total, 'page_id': page_id, 'page_size': page_size, 'coll': {}}
        return app_err_p(Error.NO_MORE_DATA, payload)
    else:
        payload = {'total': total, 'page_id': page_id, 'page_size': page_size, 'coll': list(result)}
        return app_ok_p(payload)


def level_stat(request):
    # result = cnvd_col.aggregate({'$group': {'_id': '$serverity', 'counter': {'$sum': 1}}})
    pipeline = [
        {"$group": {"_id": "$serverity", "count": {"$sum": 1}}},
    ]

    result = cnvd_col.aggregate(pipeline)
    return app_ok_p(list(result))


def month_stat(request):
    time_type = req_get_param(request, 'time_type')
    time_field = '';
    if time_type == 'submit':
        time_field = "$submitTime"
    elif time_type == 'open':
        time_field = "$openTime"
    else:
        return app_err(Error.INVALID_REQ_PARAM)

    pipeline = [
        {"$project": {"month": {"$substr": [time_field, 0, 7]}}},
        {"$group": {"_id": "$month", "month_count": {"$sum": 1}}},
        {"$sort": SON([("_id", 1)])},
    ]

    result = cnvd_col.aggregate(pipeline)
    return app_ok_p(list(result))


def discoverer_stat(request):
    pipeline = [
        {"$group": {"_id": "$discovererName", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1)])},
    ]

    result = cnvd_col.aggregate(pipeline)
    return app_ok_p(list(result))


def fix_stat(request):
    unfixed_count = cnvd_col.find({"patchName": None}).count()
    fixed_count = cnvd_col.find({"patchName": {'$regex': ".*"}}).count()
    result = {"fixed": fixed_count, "unfixed": unfixed_count}
    return app_ok_p(result)


def vul_type_stat(request):
    pipeline = [
        {"$group": {"_id": "$vulType", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1)])},
    ]

    result = cnvd_col.aggregate(pipeline)
    return app_ok_p(list(result))
