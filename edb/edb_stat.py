import common.config
from bson.son import SON

# 利用信息集合
edb_info_col = common.config.g_edb_info_col


class EdbStat:

    @staticmethod
    def verified_stat():
        pipeline = [
            {"$group": {"_id": "$verified", "count": {"$sum": 1}}},
        ]

        result = edb_info_col.aggregate(pipeline)
        stat = list(result)
        stat[0]['verified'] = ('未验证' if stat[0]['_id'] == 0 else '已验证')
        stat[1]['verified'] = ('未验证' if stat[1]['_id'] == 0 else '已验证')
        return stat

    @staticmethod
    def years_stat():
        pipeline = [
            {"$project": {"year": {"$substr": ["$date_published", 0, 4]}}},
            {"$group": {"_id": "$year", "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])},
        ]

        result = edb_info_col.aggregate(pipeline)
        stat = list(result)
        for item in stat:
            item['year'] = item['_id']
        return stat

    @staticmethod
    def platform_stat():
        pipeline = [
            {"$unwind": "$platform"},
            {"$group": {"_id": "$platform", "count": {"$sum": 1}}},
            {"$sort": SON([("_id", 1)])},
        ]

        result = edb_info_col.aggregate(pipeline)
        stat = list(result)
        for item in stat:
            item['platform'] = item['_id']['platform']
        return stat

    @staticmethod
    def type_stat():
        pipeline = [
            {"$unwind": "$type"},
            {"$group": {"_id": "$type", "count": {"$sum": 1}}},
            {"$sort": SON([("count", -1)])},
        ]

        result = edb_info_col.aggregate(pipeline)
        stat = list(result)
        for item in stat:
            item['type'] = item['_id']['name']
        return stat

