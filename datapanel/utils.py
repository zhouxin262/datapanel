def smart_decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return s.decode('gbk')
        except UnicodeDecodeError:
            return s

