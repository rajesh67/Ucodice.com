from django.conf.urls import patterns,include,url
from django.conf import settings
from .views import PostCreateView,PostUpdateView,PostDeleteView,PostListView
from plans.views import PlanCreateView,PostPlanUpdateView,PostPlanView,PostPlanFormView
from django.contrib.auth.decorators import login_required


urlpatterns=patterns('',
                    #class based views urls
                    url(r'^$',PostListView.as_view(),name="post-list"),
                    url(r'^add/$',login_required(PostCreateView.as_view(),login_url="/login/"),name="post-create"),

                    url(r'^(?P<slug>[-_\w]+)/',include([
                        url(r'^$','posts.views.post_details',name="post-details"),
                        url(r'^update/$',login_required(PostUpdateView.as_view(),login_url="/login/"),name="post-update"),
                        url(r'^delete/$',login_required(PostDeleteView.as_view(),login_url="/login/"),name="post-delete"),     
                        ])
                    ),
 )
