from django.conf.urls import patterns,url,include
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns=patterns('',
                     url(r'^$','plans.views.home',name="plans-home"),
                     url(r'^(?P<slug>[-_\w]+)/',include([
                        url(r'^plans/(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/$',login_required(PostPlanFormView.as_view(),login_url='/login/'),name="plan-create"),
                        #url(r'^plans/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/(?P<pk>[\d]+)/$','plans.views.postplan_update_view',name="continue-planning"),
                        url(r'^plans/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})/(?P<number>[0-9]+)/$',login_required(PostPlanView.as_view(),login_url='/login/'),name="continue-planning"),
                     ]),
                     )
                  	)