__author__ = 'raju'
from django import template

register = template.Library()

@register.simple_tag
def left(plan):
    arrival=int(plan.starting)*60
    left=arrival/14.40
    return left

@register.simple_tag
def width(plan):
    arrival=int(plan.starting)*60
    departure=int(plan.ending)*60
    width=((departure-arrival)/14.40)
    return width


@register.simple_tag
def arrival(plan):
    arrival=int(plan.starting)
    return arrival*60

@register.simple_tag
def departure(plan):
    arrival=int(plan.starting)
    return arrival*60


@register.simple_tag
def get_ranges(post):
    ranges=[]
    for plan in post.postplans:
        d=(plan.id,int(plan.starting)*60,int(plan.ending)*60)
        ranges.append(d)
        ranges.sort()
    ranges=sorted(ranges,key=lambda x:x[2])
    return ranges


@register.filter(name='get_intervals')
def get_intervals(post):
    ranges=get_ranges(post)
    intervals=[]
    for key,value in enumerate(ranges):
        if key!=len(ranges)-1:
            if key==0:
                if value[1]!=0:
                    range=(0,value[1])
                    intervals.append(range)
                else:
                    pass
            if value[2]==ranges[key+1][1]:
                pass
            else:
                range=(value[2],ranges[key+1][1])
                intervals.append(range)
        else:
            range=(value[2],1439)
            intervals.append(range)
    return intervals

@register.simple_tag
def get_values(dayplan):
    values=[]
    intervals=get_intervals(dayplan)
    for i in intervals:
        values.append(i[0])
        values.append(i[1])
    values.sort()
    return values


@register.simple_tag
def interval_left(interval):
    left=interval[0]
    return left/14.40

@register.simple_tag
def interval_width(interval):
    width=interval[1]-interval[0]
    return width/14.40

@register.simple_tag
def interval_name(interval):
    name=str(interval[0])+"-to-"+str(int(interval[1]))
    return name