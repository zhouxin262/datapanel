from django.conf import settings
from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)
HOUR = timedelta(hours=1)


def parse_url(url):
    url_dict = {'url': url, 'netloc': '', 'kw': ''}
    try:
        parsed_url = urlparse.urlparse(url)
        if parsed_url.netloc and parsed_url.netloc != 'www.xmeise.com':
            url_dict['netloc'] = parsed_url.netloc
            querystring = urlparse.parse_qs(parsed_url.query, True)
            if parsed_url.netloc.find('baidu') != -1:
                #baidu
                if 'wd' in querystring:
                    url_dict['kw'] = smart_decode(
                        querystring['wd'][0])
                elif 'word' in querystring:
                    url_dict['kw'] = smart_decode(
                        querystring['word'][0])
            if parsed_url.netloc.find('sogou') != -1:
                #sogou
                if 'query' in querystring:
                    url_dict['kw'] = smart_decode(
                        querystring['query'][0])
    except:
        pass
    return url_dict


def smart_decode(s):
    if s.find('%u') != -1:
        # '%u5973%u4EBA%u6210%u4EBA%u7528%u54C1' for sogou sb unicode
        return "".join([unichr(int(i, 16)) for i in s.split('%u')[1:]])
    try:
        return s.decode('utf-8', 'strict')
    except:
        try:
            return s.decode('gbk', 'strict')
        except:
            return ''


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
