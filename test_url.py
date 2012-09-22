import urlparse
url = "http://www.baidu.com/s?word=%D0%D4%D3%C3%C6%B7&tn=site888_pg&lm=-1"

parsed_url = urlparse.urlparse(url)
if parsed_url.netloc:
    referer_site = parsed_url.netloc
    referer_parsed = True
    if parsed_url.netloc in ('www.baidu.com','m.baidu.com'):
        #baidu
        querystring = urlparse.parse_qs(parsed_url.query,True)
        if querystring.has_key('wd'):
            if querystring.has_key('ie') and querystring['ie'][0] == 'utf-8':
                referer_keyword = querystring['wd'][0].decode('utf-8')
            else:
                referer_keyword = querystring['wd'][0].decode('gbk')
        elif querystring.has_key('word'):
            print querystring['word'][0].decode('gbk')
            referer_keyword = querystring['word'][0].decode('gbk').encode('utf-8')
# print referer_site, referer_keyword