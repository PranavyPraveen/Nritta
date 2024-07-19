from django import template

register = template.Library()


@register.filter()
def split_lines(value):
    if value is None:
        return []
    n = value.split('@n')

    for i in range(len(n)):
        w = n[i].split()
        w[0] = w[0].title()
        s = ' '.join(w)
        n[i] = s
    return n



