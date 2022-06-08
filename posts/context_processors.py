import datetime as dt


def time(request):
    """
    Adding timestamp variable. Usefull for cache tests
    """
    now = dt.datetime.now().timestamp()
    return {"time": now}
