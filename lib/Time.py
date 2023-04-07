from datetime import datetime
import pytz
#该函数用于将utc时间转换为cst时间
def utc_to_cst(utc_time):
    datetime_obj = datetime.strptime(utc_time,'%Y-%m-%dT%H:%M:%S.%fZ')
    utc_timezone = pytz.timezone('UTC')
    cst_timezone = pytz.timezone('Asia/Shanghai')
    utc_datetime = utc_timezone.localize(datetime_obj)
    cst_datetime = utc_datetime.astimezone(cst_timezone)
    return cst_datetime.strftime('%Y-%m-%d %H:%M:%S')