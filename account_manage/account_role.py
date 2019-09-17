from common.utils.general import enum

role = [
    0,
    1,
    2,
    3,
]
Acc_Role = enum(
    'NO_ROLE',
    'ADMIN',
    'AUDITOR',
    'OPERATOR',
)
