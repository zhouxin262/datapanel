# coding=utf-8
import urlparse
import re
import chardet
from datetime import tzinfo, timedelta, datetime

from django.conf import settings

ZERO = timedelta(0)
HOUR = timedelta(hours=1)


class RunFunctions():
    def ecs_order(self, param):
        from ecshop.models import OrderInfo
        OrderInfo.objects.process(**param)

    def ecs_orderstatus(self, param):
        from ecshop.models import OrderInfo
        OrderInfo.objects.process(**param)

    def ecs_goods(self, param):
        from ecshop.models import Goods
        Goods.objects.process(**param)

    def ecs_del_order(self, param):
        from ecshop.models import OrderInfo, OrderGoods
        o = OrderInfo.objects.get(order_sn=param["order_sn"])
        OrderGoods.objects.filter(order=o).delete()
        o.delete()


class Group():
    FromModel = None
    ToModel = None

    static_attr = {}
    dynamic_attr = {}
    function_attr = {}
    exclude_attr = []
    annotate = {}
    fargs = {}
    eargs = {}
    exargs = {}
    values = []

    def __init__(self, FromModel, ToModel):
        self.FromModel = FromModel
        self.ToModel = ToModel

    def easy_group(self, update=False):
        static_attr = self.static_attr
        dynamic_attr = self.dynamic_attr
        function_attr = self.function_attr
        exclude_attr = self.exclude_attr
        values = self.values
        annotate = self.annotate
        fargs = self.fargs
        eargs = self.eargs
        exargs = self.exargs

        exclude_attr.extend([v for v in dynamic_attr.values()])

        if static_attr and annotate:
            # clean db
            if not update:
                # delete & bulk_create, most rapidly
                self.ToModel.objects.filter(**static_attr).delete()

                if values:
                    # group
                    dataset = self.FromModel.objects.filter(
                        **fargs).extra(**eargs).exclude(**exargs).values(*values).annotate(**annotate)
                    data = []
                    for datarow in dataset:
                        obj = self.ToModel()
                        for k, v in static_attr.items():
                            setattr(obj, k, v)
                        for k, v in dynamic_attr.items():
                            setattr(obj, k, datarow[v])
                        for i in values:
                            if i not in exclude_attr:
                                setattr(obj, i, datarow[i])
                        for i in annotate.keys():
                            if i not in exclude_attr:
                                setattr(obj, i, datarow[i])
                        for k, v in function_attr.items():
                            setattr(obj, k, v(datarow))
                        data.append(obj)

                    # insert into db
                    self.ToModel.objects.bulk_create(data)
                else:
                    datarow = self.FromModel.objects.filter(**fargs).extra(**eargs).exclude(**exargs).aggregate(**annotate)
                    obj = self.ToModel()
                    for k, v in static_attr.items():
                        setattr(obj, k, v)
                    for k, v in dynamic_attr.items():
                        setattr(obj, k, datarow[v])
                    for i in annotate.keys():
                        if i not in exclude_attr:
                            setattr(obj, i, datarow[i])
                    for k, v in function_attr.items():
                        setattr(obj, k, v(datarow))
                    obj.save()
            else:
                # update, for one table's content has to groupby twice
                if values:
                    # group
                    dataset = self.FromModel.objects.filter(
                        **fargs).extra(**eargs).exclude(**exargs).values(*values).annotate(**annotate)
                    data = []
                    for datarow in dataset:
                        get_or_create_args = {}
                        for k, v in static_attr.items():
                            get_or_create_args[k] = v
                        for k, v in dynamic_attr.items():
                            get_or_create_args[k] = datarow[v]
                        for i in values:
                            if i not in exclude_attr:
                                get_or_create_args[i] = datarow[i]
                        for k, v in function_attr.items():
                            get_or_create_args[k] = v(datarow)
                        obj = self.ToModel.objects.get_or_create(**get_or_create_args)[0]
                        for i in annotate.keys():
                            if i not in exclude_attr:
                                setattr(obj, i, datarow[i])
                        obj.save()
                else:
                    datarow = self.FromModel.objects.filter(**fargs).extra(**eargs).exclude(**exargs).aggregate(**annotate)
                    get_or_create_args = {}
                    for k, v in static_attr.items():
                        get_or_create_args[k] = v
                    for k, v in dynamic_attr.items():
                        get_or_create_args[k] = datarow[v]
                    for k, v in function_attr.items():
                        get_or_create_args[k] = v(datarow)
                    obj = self.ToModel.objects.get_or_create(**get_or_create_args)[0]
                    for i in annotate.keys():
                        if i not in exclude_attr:
                            setattr(obj, i, datarow[i])
                    obj.save()
        else:
            print "missing arguments"


def get_times(interval):
    times = []
    datetype = 'hour'
    if interval == 1:
        datetype = 'hour'
        for i in range(24):
            t = now().replace(hour=0, minute=0, second=0,
                              microsecond=0) - timedelta(hours=i + 1)
            times.append(t)
    elif interval == 7 or interval == 30:
        datetype = 'day'
        for i in range(interval):
            t = now().replace(hour=0, minute=0, second=0,
                              microsecond=0) - timedelta(days=i + 1)
            times.append(t)
    return (datetype, times)


def parse_url(url):
    url_dict = {'u': url, 'd': '', 'kw': ''}
    # try:
    parsed_url = urlparse.urlparse(url)
    if parsed_url.netloc and parsed_url.netloc != 'www.xmeise.com':
        url_dict['d'] = parsed_url.netloc
        querystring = urlparse.parse_qs(parsed_url.query, True)
        if parsed_url.netloc.find('baidu') != -1:
            # baidu
            if 'wd' in querystring:
                url_dict['kw'] = decode_keyword(
                    querystring['wd'][0])
            elif 'word' in querystring:
                url_dict['kw'] = decode_keyword(
                    querystring['word'][0])
        if parsed_url.netloc.find('sogou') != -1:
            # sogou
            if 'query' in querystring:
                url_dict['kw'] = decode_keyword(
                    querystring['query'][0])
    # except:
        # pass
    return url_dict


def decode_keyword(s):
    s = s.strip()
    if s.find('%u') != -1:
        # '%u5973%u4EBA%u6210%u4EBA%u7528%u54C1' for sogou sb unicode
        res = "".join([unichr(int(i, 16)) for i in s.split('%u')[1:]])
    else:
        try:
            res = s.decode(chardet.detect(s)['encoding'])
        except:
            res = ''

    # res = res.replace('site:', '')
    p = re.compile('[\(\)\+\;\,\>\<\\\ ]')
    res = p.sub('', res, re.U)
    return res


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
