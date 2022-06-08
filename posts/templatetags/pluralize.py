from django import template

register = template.Library()


@register.filter
def rupluralize(value: int, arg: str) -> str:
    """
        Example: print(5, rupluralize(5, 'стул,стула,стульев'))
        > 5 стульев
    """
    args = arg.split(',')
    try:
        number = abs(int(value))
    except TypeError:
        number = 0

    digit = number % 10
    decs = number % 100

    if digit == 1 and decs != 11:
        return args[0]
    elif 2 <= digit <= 4 and (decs < 10 or decs >= 20):
        return args[1]
    return args[2]
