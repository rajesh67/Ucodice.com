from django import template
import datetime


register=template.Library()

@register.simple_tag(name="cut")
def cut(value,arg):
    url="/"+value+"/"+arg+"/"
    return url