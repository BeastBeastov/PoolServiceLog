from django import template

register = template.Library()

@register.simple_tag
def color_sh(status):
    if status == 'A':
        return f'background-color: #FF0000; color: #B0E0E6'
    elif status == 'B':
        return f'background-color: #FF8C00; color: #00008B'
    elif status == 'C':
        return f'background-color: #00FF7F; color: #800080'
    elif status == 'D':
        return f'background-color: #00BFFF; color: #FFFF00'

