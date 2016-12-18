from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from library.log import rbe_logger
from organizations.forms import OrganizationDescriptionForm
from organizations.models import Organization, OrganizationUser, OrganizationDescription, OrganizationCheck


def create_organization(name, website_url):
    org = Organization(name=name, website_url=website_url)
    org.save()

    od = OrganizationDescription(organization=org)
    od.save()

    oc = OrganizationCheck(organization=org)
    oc.save()

    return org


def overview(request):
    context = {
        'organizations': Organization.objects.filter(enabled=True).order_by('name')
    }
    return render(request, 'organizations/overview.html', context)


@login_required
def details(request, organization_id):
    """ Shows the details of an organization """
    try:
        organization = Organization.objects.get(id=organization_id, enabled=True)
    except Organization.DoesNotExist:
        return render(request, 'general/error_page.html')

    ou = OrganizationUser.objects.filter(user=request.user, organization=organization)
    view_role = ou.first().level if ou.exists() else None
    context = {
        'view_role': view_role,
        'organization': organization
    }

    return render(request, 'organizations/details.html', context)


@login_required
def edit(request, organization_id):
    """ Lets an editor change the description of an organization """
    try:
        organization = Organization.objects.get(id=organization_id)
    except Organization.DoesNotExist:
        rbe_logger.info("Organization with id={} not found or was not enabled".format(organization_id))
        return render(request, 'general/error_page.html')

    ou_qs = OrganizationUser.objects.filter(organization=organization, user=request.user)

    if not ou_qs.exists() or ou_qs.first().level != 'Editor':
        rbe_logger.info("User {} tried to access edit function for oid={} but was not allowed".format(request.user, organization_id))
        return render(request, 'general/access_error.html')

    if request.method == 'POST':
        form = OrganizationDescriptionForm(request.POST, instance=organization.organizationdescription)

        if form.is_valid():
            organization_description = form.instance
            organization_description.save()
            return redirect(reverse('organization-details', kwargs={'organization_id': organization.id}))
    else:
        form = OrganizationDescriptionForm(instance=organization.organizationdescription)

    return render(request, 'organizations/edit.html', {
        'form': form,
        'organization': organization
    })
