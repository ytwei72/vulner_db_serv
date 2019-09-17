import common.config
from common.response import app_ok_p, app_err_p, app_ok, app_err
from common.error_code import Error
from common.utils.general import SysUtils

from account_manage.account_status import status, Acc_Status
from account_manage.account_role import role, Acc_Role

mongo_client = common.config.g_mongo_client
# 系统管理数据库
sys_manage_db = common.config.g_sys_manage_db
# 账户集合
accounts_col = common.config.g_accounts_col

PASSWORD_MAT = 5
VALID_YEARS = 1


class Accounts:
    @staticmethod
    def fetch_brief(account):
        acc_brief = accounts_col.find_one(
            {'account': account},
            {'_id': 0, 'account': 1, 'status': 1, 'role': 1, 'create_time': 1, 'expire_time': 1}
        )
        return acc_brief

    @staticmethod
    def fetch_pwd_params(account):
        pwd_params = accounts_col.find_one(
            {'account': account},
            {'_id': 0, 'account': 1, 'status': 1, 'role': 1, 'pwd_mat': 1, 'pwd_rat': 1, 'password': 1}
        )
        return pwd_params

    @staticmethod
    def update(account, update_items):
        update_res = accounts_col.update_one({'account': account}, {'$set': update_items})
        return update_res

    @staticmethod
    def exist(account):
        exist_acc = Accounts.fetch_brief(account)
        return exist_acc is not None, exist_acc

    @staticmethod
    def register(acc_info):
        # 检查账户是否已存在
        exist, acc_brief = Accounts.exist(acc_info.get('account'))
        if exist:
            return Error.ACC_REGISTERED, acc_brief

        # 设置账户为未激活的操作员角色
        acc_info['status'] = Accounts.get_status_int(Acc_Status.ACC_INACTIVE)
        acc_info['role'] = Accounts.get_role_int(Acc_Role.OPERATOR)

        # 生成密码盐，并生成加密的密码
        # 设置密码最大尝试次数和剩余尝试次数
        acc_info['pwd_mat'] = acc_info['pwd_rat'] = PASSWORD_MAT

        # 设置账户创建时间和失效时间
        acc_info['create_time'] = SysUtils.get_now_time()
        acc_info['expire_time'] = SysUtils.get_time_delta_years(1)

        # 添加一条新账户数据
        res = accounts_col.insert_one(acc_info)
        if res.inserted_id is None:
            return Error.FAIL_CREATE_ACC

        # 读取刚创建的账户简要信息
        acc_brief = Accounts.fetch_brief(acc_info.get('account'))
        return Error.OK, acc_brief

    @staticmethod
    def update_info(account, info):
        # 检查账户是否存在
        exist, acc_brief = Accounts.exist(account)
        if not exist:
            return Error.ACC_NOT_FOUND, acc_brief

        # res = Accounts.update(account, {'status': active})
        # 更新该账户信息
        res = Accounts.update(account, info)
        if res.matched_count != 1:
            return Error.INTERNAL_EXCEPT, acc_brief

        # 读取账户简要信息
        acc_brief = Accounts.fetch_brief(account)
        return Error.OK, acc_brief

    @staticmethod
    def verify_password(account, password):
        # 检查账户是否存在
        exist, acc_brief = Accounts.exist(account)
        if not exist:
            return Error.ACC_NOT_FOUND, acc_brief

        # 查询密码参数
        pwd_params = Accounts.fetch_pwd_params(account)

        # 是否已锁定
        if pwd_params['pwd_rat'] == 0:
            acc_brief.update({'pwd_mat': pwd_params['pwd_mat'], 'pwd_rat': pwd_params['pwd_rat']})
            return Error.PASSWORD_LOCKED, acc_brief

        # 判断待校验的密码是否正确
        if pwd_params['password'] == password:
            # 恢复剩余尝试次数
            res = Accounts.update(account, {'pwd_rat': pwd_params['pwd_mat']})
            if res.matched_count != 1:
                return Error.INTERNAL_EXCEPT, acc_brief
            else:
                acc_brief.update({'pwd_mat': pwd_params['pwd_mat'], 'pwd_rat': pwd_params['pwd_mat']})
                return Error.OK, acc_brief
        else:
            # 校验失败，剩余次数减1
            rat = pwd_params['pwd_rat'] - 1
            res = Accounts.update(account, {'pwd_rat': rat})
            if res.matched_count != 1:
                return Error.INTERNAL_EXCEPT, acc_brief
            acc_brief.update({'pwd_mat': pwd_params['pwd_mat'], 'pwd_rat': rat})
            # 剩余次数为0返回锁定错误，否则返回校验失败
            if rat == 0:
                return Error.PASSWORD_LOCKED, acc_brief
            else:
                return Error.FAIL_VERIFY_PASSWORD, acc_brief

    @staticmethod
    def get_status_int(acc_status):
        return status[acc_status]

    @staticmethod
    def get_role_int(acc_role):
        return role[acc_role]
