from django.conf.urls import url

import public.views

urlpatterns = [
    url(r'general', public.views.general, name="information"),
    url(r'developer', public.views.developer, name="developer"),
    url(r'metrics', public.views.metrics, name="metrics")
]