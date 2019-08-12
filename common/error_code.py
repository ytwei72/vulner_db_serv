from enum import Enum, unique
from common.utils.general import enum

err = [
    {'code': 0, 'msg': '成功'},
    {'code': 1002, 'msg': '系统内部异常'},
    {'code': 1003, 'msg': '未查询到数据'},
    {'code': 9999, 'msg': '未知错误'},
]

Error = enum(
    'OK',
    'INTERNAL_EXCEPT',
    'NO_MORE_DATA',
    'UNKNOWN',
)


# @unique
# class Error(Enum):
#     OK = 0
#     UNKNOWN = 1


def get_err(error):
    return err[error]
