import core.developer_views

from django.conf.urls import patterns, url


urlpatterns = [
     url(r'info/$',  core.developer_views.info, name='developer_info'),
     url(r'v1/username/$',  core.developer_views.protected_api, name='developer_api_test'),
]
