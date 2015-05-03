import calendar

__author__ = 'dvpermyakov'


def timestamp(datetime_object):
    return calendar.timegm(datetime_object.timetuple())
