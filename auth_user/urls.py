__author__ = 'kctheng'
from django.conf.urls import include, url, patterns
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as tokenview
from auth_user import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'magstreet_abstract.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'auth_user.views.default'),
    url(r'^users/$', views.user_list.as_view()),
    url(r'^users/(?P<pk>[0-9]+)$', views.user_detail.as_view()),
    url('', include('social.apps.django_app.urls', namespace='social')),

]


urlpatterns += [
    url(r'^api-token-auth/', tokenview.obtain_auth_token),
    url(r'^rest-auth/facebook/$', views.FacebookLogin2.as_view(), name='fb_login')
]

urlpatterns = format_suffix_patterns(urlpatterns)