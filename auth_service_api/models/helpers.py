# -*- coding: utf-8 -*-
# @Time    : 03/02/2021 12:57
# @Author  : Aydar
# @FileName: helpers.py
# @Software: PyCharm
# @Telegram   ：aydardev

from pytz import timezone
import datetime
from auth_service_api.config import TIME_ZONE

tz = timezone(TIME_ZONE)

class DateTime(object):
    def __init__(self, date_time: datetime = None):
        self.date_time = date_time

    def __add__(self, other):
        return self.date_time + other.date_time

    @staticmethod
    def now():
        return datetime.datetime.now(tz)
    
    @staticmethod
    def timezone():
        return datetime.datetime.now(tz).tzname()
    
    @staticmethod
    def timedelta(d=0, s=0, mics=0, mills=0, m=0, h=0, w=0):
        """
        Args:
            d (int, days): [days]. Defaults to 0.
            s (int, seconds): [seconds]. Defaults to 0.
            mics (int, microseconds): [microseconds]. Defaults to 0.
            mills (int, milliseconds): [milliseconds]. Defaults to 0.
            m (int, minutes): [descminutesription]. Defaults to 0.
            h (int, hours): [hours]. Defaults to 0.
            w (int, weeks): [weeks]. Defaults to 0.

        Returns:
            datetime: [returned datetime.timedelta]
        """
        return datetime.timedelta(days=d, seconds=s, microseconds=mics, milliseconds=mills, minutes=m, hours=h, weeks=w)
