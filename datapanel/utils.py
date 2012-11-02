from django.conf import settings
from datetime import tzinfo, timedelta, datetime


def smart_decode(s):
    try:
        # '%u5973%u4EBA%u6210%u4EBA%u7528%u54C1' for sogou sb unicode
        return "".join([unichr(int(i, 16)) for i in s.split('%u')[1:]])
    except:
        try:
            return s.decode('utf-8', 'strict')
        except:
            try:
                return s.decode('gbk', 'strict')
            except:
                return ''

ZERO = timedelta(0)
HOUR = timedelta(hours=1)


def now():
    if settings.USE_TZ:
        return datetime.now(UTC())
    else:
        return datetime.now()


def today_str(format="%Y-%m-%d"):
    return now().strftime(format)


class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
