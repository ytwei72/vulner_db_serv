from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.http_request import req_get_param_int, req_get_param, req_post_param, req_post_param_int, req_post_param_dict
import common.config

from common.utils.general import SysUtils
from account_manage.accounts import Accounts

from bson.son import SON


def register_account(request):
    params = req_post_param_dict(request)
    account_info = SysUtils.copy_dict(params, ['account', 'password', 'name', 'phone', 'address', 'email',
                                               'description', ])
    err, acc = Accounts.register(acc_info=account_info)
    return app_err_p(err, acc)


def activate_account(request):
    account = req_post_param(request, 'account')
    active = req_post_param_int(request, 'active')
    err, acc = Accounts.update_info(account, {'status': active})
    return app_err_p(err, acc)


def set_account_role(request):
    account = req_post_param(request, 'account')
    role = req_post_param_int(request, 'role')
    err, acc = Accounts.update_info(account, {'role': role})
    return app_err_p(err, acc)


def verify_password(request):
    account = req_post_param(request, 'account')
    password = req_post_param(request, 'password')
    err, acc = Accounts.verify_password(account, password)
    return app_err_p(err, acc)


def unlock_account(request):
    account = req_post_param(request, 'account')
    password = req_post_param(request, 'password')
    pwd_params = Accounts.fetch_pwd_params(account)
    err, acc = Accounts.update_info(account, {'password': password, 'pwd_rat': pwd_params['pwd_mat']})
    return app_err_p(err, acc)
