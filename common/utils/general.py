from dateutil.relativedelta import relativedelta
import json
from datetime import date, datetime, timedelta


def enum(*args):
    enums = dict(zip(args, range(len(args))))
    return type('Enum', (), enums)


class SysUtils:
    @staticmethod
    def get_now_time():
        return datetime.now()

    @staticmethod
    def get_time_delta_days(delta_days):
        now = datetime.now()
        new_time = now + timedelta(days=delta_days)
        return new_time

    @staticmethod
    def get_time_delta_years(delta_years):
        now = datetime.now()
        new_time = now + relativedelta(years=delta_years)
        return new_time

    @staticmethod
    def print_time(time):
        print(time)

    @staticmethod
    def copy_dict(src_dict, key_list):
        dest_dict = {}
        for key in key_list:
            if key in src_dict.keys():
                dest_dict[key] = src_dict[key]
            else:
                dest_dict[key] = ''
        return dest_dict

    @staticmethod
    def grid_out_to_dict(grid_out):
        if grid_out is None:
            return None
        dest_dict = {'filename': grid_out.filename, 'aliases': grid_out.aliases[0],
                     'content_type': grid_out.content_type, 'length': grid_out.length, 'name': grid_out.name}
        # dest_dict['content'] = grid_out.read()
        return dest_dict


class TimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
