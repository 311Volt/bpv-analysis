import datetime


def str_to_datetime(t: str):
    return datetime.datetime.strptime(t, "%Y-%m-%d %H:%M")


def datetime_to_str(t: datetime.datetime):
    return t.strftime("%Y-%m-%d %H:%M")
