import pymongo

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
g_exploit_db = g_mongo_client["exploit_db"]
# 漏洞利用信息集合
g_edb_info_col = g_exploit_db["exploit_info"]
# 漏洞利用方法文件存储桶
g_edb_method_bucket = g_exploit_db["exploit_methods"]
