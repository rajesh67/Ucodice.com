
from django.db import models
from mongoengine.django.auth import User
# Create your models here.
from Ucodice.settings import POSTDB, PLANDB
from mongoengine import *
import datetime
from django.utils.text import slugify
from django.core.urlresolvers import reverse

connect(POSTDB)
from plans.models import PostPlan,Plan


class Post(Document):
    posted_by=ReferenceField(User)
    planner=ReferenceField(User)
    title=StringField(max_length=300)

    slug=StringField(unique=True)

    posted_on=DateTimeField(default=datetime.datetime.now())
    destination=StringField(max_length=50)
    arrival=DateTimeField(default=datetime.datetime.now())
    departure=DateTimeField()

    description=StringField()
    duration=IntField(default=0,help_text="choose duration in days")

    bidders=ListField(ReferenceField(User))
    postplans=ListField(ReferenceField(PostPlan))

    def __unicode__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        if self.duration and self.arrival:
            self.departure=self.arrival+datetime.timedelta(days=self.duration)
        else:
            return "please provide a duration in days"
        return super(Post,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('post-details',kwargs={'slug':self.slug})
