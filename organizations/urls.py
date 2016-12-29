from django.conf.urls import url

import organizations.views

urlpatterns = [
    url(r'overview$', organizations.views.overview, name="organization-overview"),
    url(r'organizations', organizations.views.organizations, name="organization-list"),
    url(r'details/(?P<organization_id>\d*)$', organizations.views.details, name="organization-details"),
    url(r'edit/(?P<organization_id>\d*)$', organizations.views.edit, name="organization-edit"),
    url(r'create', organizations.views.create_organization, name="organization-create"),
    url(r'post/(?P<organization_id>\d*)$', organizations.views.create_post, name="organization-post"),
]