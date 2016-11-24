from django.conf import settings
from core.models import Toggles


def additional_template_vars(request):
    return {
        'gtracking_id': settings.GOOGLE_ANALYTICS_ID
    }

def toggles(request):
    all_toggle_names = Toggles.all_toggle_names()

    toggle_parameters = {
        'toggles': {}
    }

    if hasattr(request, 'user') and request.user.is_authenticated():
        for toggle_name in all_toggle_names:
            toggle_parameters['toggles'][toggle_name] = Toggles.is_active(toggle_name, request.user)

    return toggle_parameters