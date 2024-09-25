from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='to_currency')
def to_currency(field, lang):
    if lang == "fr":
        return f"{field} €"
    return f"{field} $"