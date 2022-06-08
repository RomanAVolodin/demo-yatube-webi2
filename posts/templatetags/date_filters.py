from django import template
from datetime import datetime as dt


register = template.Library()

months = [
    'января',
    'февраля',
    'марта',
    'апреля',
    'мая',
    'июня',
    'июля',
    'августа',
    'сентября',
    'ноября',
    'декабря',
]


@register.filter
def datetime_ru_long(value: dt) -> str:
    """
    Reformat datetime in Russ-readable format
    Example: 08 июня 2020 г. 08:12
    @param value: datetime
    @return: str
    """
    if not isinstance(value, dt):
        return str(value)
    month_name = months[int(value.strftime('%m')) - 1]
    return f"{value.strftime('%d')} {month_name} {value.strftime('%Y')} г. " \
           f"{value.strftime('%H:%M')}"
