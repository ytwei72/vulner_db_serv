import pymongo
from gridfs import GridFS

# edb采用标准数据库还是小数据库
# 1：标准数据库；2：小数据库；
EDB_TYPE = 1

# mongo-db客户端
g_mongo_client = pymongo.MongoClient("mongodb://admin:123456@192.168.182.88:27017/")

# 系统管理数据库
g_sys_manage_db = g_mongo_client["system_manage"]
# 账户集合
g_accounts_col = g_sys_manage_db["accounts"]

# cnvd 数据库
g_cnvd_db = g_mongo_client["cnvd_share"]
# cnvd 集合
g_cnvd_col = g_cnvd_db["cnvd_share"]

# edb 数据库
g_exploit_db_full = g_mongo_client["exploit_db"]
# 漏洞利用信息集合
g_edb_info_col_full = g_exploit_db_full["exploit_info"]
# 漏洞利用方法文件存储桶
g_edb_method_fs_full = GridFS(g_exploit_db_full, collection='exploit_methods')
# author，type，platform 的信息集合
g_author_coll_full = g_exploit_db_full["edb_author"]
g_type_coll_full = g_exploit_db_full["edb_type"]
g_platform_coll_full = g_exploit_db_full["edb_platform"]

# edb 数据库子集
g_exploit_db_tiny = g_mongo_client["exploit_db_tiny"]
# 漏洞利用信息集合-子集
g_edb_info_col_tiny = g_exploit_db_tiny["exploit_info_tiny"]
# 漏洞利用方法文件存储桶-子集
g_edb_method_fs_tiny = GridFS(g_exploit_db_tiny, collection='exploit_methods_tiny')
# author，type，platform 的信息集合
g_author_coll_tiny = g_exploit_db_tiny["edb_author"]
g_type_coll_tiny = g_exploit_db_tiny["edb_type"]
g_platform_coll_tiny = g_exploit_db_tiny["edb_platform"]

if EDB_TYPE == 1:
    # 完整数据库
    g_exploit_db = g_exploit_db_full
    g_edb_info_col = g_edb_info_col_full
    g_edb_method_fs = g_edb_method_fs_full
    g_author_coll = g_author_coll_full
    g_type_coll = g_type_coll_full
    g_platform_coll = g_platform_coll_full
elif EDB_TYPE == 2:
    # 小数据库
    g_exploit_db = g_exploit_db_tiny
    g_edb_info_col = g_edb_info_col_tiny
    g_edb_method_fs = g_edb_method_fs_tiny
    g_author_coll = g_author_coll_tiny
    g_type_coll = g_type_coll_tiny
    g_platform_coll = g_platform_coll_tiny
else:
    # 默认用小数据库
    g_exploit_db = g_exploit_db_tiny
    g_edb_info_col = g_edb_info_col_tiny
    g_edb_method_fs = g_edb_method_fs_tiny
    g_author_coll = g_author_coll_tiny
    g_type_coll = g_type_coll_tiny
    g_platform_coll = g_platform_coll_tiny
