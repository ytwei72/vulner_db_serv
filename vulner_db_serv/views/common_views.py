
from common.session import UserSession
from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param, req_post_param, req_post_param_int, \
    req_post_param_dict


def set_user(request):
    uuid = req_get_param(request, 'uuid')
    account = req_get_param(request, 'account')
    name = req_get_param(request, 'name')
    UserSession.set_user(uuid, account, name)
    return app_ok()


def get_user(request):
    uuid, account, name = UserSession.get_user()
    return app_ok_p({'uuid': uuid, 'account': account, 'name': name})
