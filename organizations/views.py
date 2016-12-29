from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from library.log import rbe_logger
from library.mail.SendgridEmailClient import SendgridEmailClient
from organizations.forms import OrganizationDescriptionForm, OrganizationCreateForm, OrganizationPostForm
from organizations.mail import OrganizationCreateNotification
from organizations.models import Organization, OrganizationUser, OrganizationDescription, OrganizationCheck, \
     OrganizationPost, ROLE_CHOICES


def _create_organization(name, website_url):
    org = Organization(name=name, website_url=website_url)
    org.save()

    od = OrganizationDescription(organization=org)
    od.save()

    oc = OrganizationCheck(organization=org)
    oc.save()

    return org


def overview(request):
    op = OrganizationPost.objects.filter(organization__enabled=True).order_by('-created')[0:10]
    context = {
        'organization_posts': op
    }

    return render(request, 'organizations/overview.html', context)


def organizations(request):
    organizations = Organization.objects.filter(enabled=True).order_by('name')
    context = {
        'organizations': organizations
    }
    return render(request, 'organizations/organizations.html', context)


def details(request, organization_id):
    """ Shows the details of an organization """
    try:
        organization = Organization.objects.get(id=organization_id, enabled=True)
    except Organization.DoesNotExist:
        return render(request, 'general/error_page.html')

    if request.user.is_authenticated():
        ou = OrganizationUser.objects.filter(user=request.user, organization=organization)
        view_role = ou.first().level if ou.exists() else None
    else:
        view_role = None

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


@login_required
def create_organization(request):
    """ Lets a user create an organization """

    if request.method == 'POST':
        form = OrganizationCreateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            website_url = form.cleaned_data['website']
            contact_email = form.cleaned_data['contact_email']

            organization = _create_organization(name, website_url)
            organization.enabled = False
            organization.contact_email = contact_email
            organization.save()

            ou = OrganizationUser(organization=organization, level=ROLE_CHOICES[0][0], user=request.user)
            ou.save()

            try:
                sec = SendgridEmailClient()
                sec.send_mail(OrganizationCreateNotification(organization))
            except Exception as e:
                rbe_logger.exception(e)

            return render(request, 'organizations/create.html', {'form': None, 'status': 'created'})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrganizationCreateForm()

    return render(request, 'organizations/create.html', {'form': form})


@login_required
def create_post(request, organization_id):
    """ Lets a user create an post """
    if organization_id == '':
        org_list = OrganizationUser.objects.filter(user=request.user, level=ROLE_CHOICES[0][0]).values_list('organization', flat=True)
        org_list = Organization.objects.filter(id__in=org_list)
        return render(request, 'organizations/pre_post.html', {'organizations': org_list})

    try:
        organization = Organization.objects.get(id=organization_id)
    except Organization.DoesNotExist:
        return render(request, 'organizations/post.html', {'form': None, 'error': 'organization_not_found'})

    ou_qs = OrganizationUser.objects.filter(organization=organization, user=request.user, level=ROLE_CHOICES[0][0])

    # Check if the user is allowed to post as a representative for an organization
    if ou_qs.exists():
        if request.method == 'POST':
            form = OrganizationPostForm(request.POST)
            if form.is_valid():

                if not organization.can_post:
                    form.add_error(None, "Organization posted recently - can only post every {} hours!".format(settings.POSTING_TIMEOUT_HOURS))
                elif not organization.enabled:
                    form.add_error(None, "Organization not enabled - cannot post!")
                else:
                    content = form.cleaned_data['content']
                    user = request.user
                    current_time = timezone.now()

                    op = OrganizationPost(organization=organization, content=content, author=user, created=current_time)
                    op.save()

                    return redirect('organization-overview')
        else:
            form = OrganizationPostForm()

        return render(request, 'organizations/post.html', {'form': form, 'organization': organization})
    else:
        return render(request, 'organizations/post.html', {'form': None, 'error': 'not_an_editor'})