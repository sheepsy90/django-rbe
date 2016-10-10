from django.conf import settings


def additional_template_vars(request):
    return {
        'gtracking_id': settings.GOOGLE_ANALYTICS_ID
    }
