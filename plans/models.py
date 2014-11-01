from django.db import models

from mongoengine.django.auth import User

# Create your models here.
from mongoengine import *
import datetime
from Ucodice.settings import PLANDB
from django.core.urlresolvers import reverse
connect(PLANDB)

class Plan(EmbeddedDocument):
    starting=DateTimeField()
    ending=DateTimeField()

    title=StringField(max_length=200)
    transport=StringField(max_length=200)
    cost=DecimalField(default=100)

    content=StringField(max_length=500)
    links=ListField(URLField(),)
    pictures=ListField(ImageField(),)

    def __unicode__(self):
        return self.title

class PostPlan(Document):
    date=DateTimeField()
    starting=DecimalField(required=True)
    ending=DecimalField(required=True)

    title=StringField(max_length=200)
    transport=StringField(max_length=200)
    cost=DecimalField(default=100)

    content=StringField(max_length=500)
    links=ListField(URLField(),)
    pictures=ListField(ImageField(),)

