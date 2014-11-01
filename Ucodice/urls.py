from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from posts.views import UserCreationView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Ucodice.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$','posts.views.login_view',name="login"),
    url(r'^signup/$',UserCreationView.as_view(),name="register"),
    url(r'^users/(?P<pk>[0-9]+)/$','posts.views.user_profile',name="user-profile"),
    url(r'^plans/',include('plans.urls')),
    url(r'^posts/',include('posts.urls')),
    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
