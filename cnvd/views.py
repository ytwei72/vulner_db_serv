from common.response import app_ok_p, app_err_p, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int
import pymongo

mongo_client = pymongo.MongoClient("mongodb://admin:123456@192.168.137.88:27017/")
# cnvd 数据库
cnvd_db = mongo_client["cnvd_share"]
# cnvd 集合
cnvd_col = cnvd_db["cnvd_share"]


def index(request):
    return app_ok_p("Hello, you're at the CNVD index.")


def retrieve(request):
    return app_err_p(Error.INTERNAL_EXCEPT, "Hello, world. You're at the CNVD index.")


def fetch(request):
    page_id = req_get_param_int(request, 'page_id')
    page_size = req_get_param_int(request, 'page_size')
    exist_item = cnvd_col.find_one({"number": 'CNVD-2016-08468'})
    result = cnvd_col.find({"number": {'$exists': True}}, {'_id': 0}).skip(page_id * page_size).limit(page_size)
    # result = cnvd_col.find({"number": {'$exists': True}}, {'_id': 0})
    if result.count() == 0:
        return app_err(Error.NO_MORE_DATA)
    else:
        return app_ok_p(list(result))
