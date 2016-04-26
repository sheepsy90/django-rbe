from django.conf.urls import patterns, include, url
from django.contrib import admin
import inventory

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_rbe_inventory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^inventory/', include('inventory.urls'))
)
