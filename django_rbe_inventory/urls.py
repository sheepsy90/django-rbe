import core.views
from django.conf.urls import patterns, include, url
from django.contrib import admin
import inventory

urlpatterns = patterns('',
    # Examples:
    url(r'^$', core.views.login, name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^core/', include('core.urls')),
    url(r'^profile/', include('profile.urls'))
)
