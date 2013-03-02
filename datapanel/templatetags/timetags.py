from django import template
register = template.Library()


def time2stamp(time):
    try:
        # assume, that timestamp is given in seconds with decimal point
        ts = int(time)
    except ValueError:
        return None
    return str(ts * 1000)
register.filter(time2stamp)
