from datetime import tzinfo, timedelta, datetime

def smart_decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return s.decode('gbk')
        except UnicodeDecodeError:
            return s

ZERO = timedelta(0)
HOUR = timedelta(hours=1)

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO