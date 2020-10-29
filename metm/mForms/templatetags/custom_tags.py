from django import template
register = template.Library()

@register.simple_tag
def return_options(options):
    print(options)