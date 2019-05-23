from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^chat/', include('chat.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^api/users/', include('accounts.urls')),
]
