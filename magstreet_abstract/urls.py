from django.conf.urls import include, url, patterns
from django.contrib import admin
from auth_user import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'magstreet_abstract.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('auth_user.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/v1/', include('rest_auth.urls')),
    # url(r'^api/v1/register/', 'auth_user.views.register_user'),
    url(r'^api/v1/register/', views.RegisterUser.as_view()),
    url(r'^api/v1/token/check/', views.check_token.as_view()),
    url(r'^api/v1/facebook_login/', views.FacebookLogin.as_view()),
    #url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
]

