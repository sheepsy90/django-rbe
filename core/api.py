from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from oidc_provider.lib.utils.oauth2 import protected_resource_view

from core.models import EmailVerification


@require_http_methods(['GET'])
@protected_resource_view(['identity'])
def identity(request, *args, **kwargs):
    """ This endpoint provides the identity of a user given a correct API token.
        :return: {'uid': <int: user_id>, 'username': <str: username>, 'email': <str: email>}
    """
    if 'token' not in kwargs:
        return HttpResponse("Provide a token", status=403)

    token = kwargs['token']

    email_verified = EmailVerification.objects.get(user=token.user).confirmed

    dic = {
        'uid': token.user.id,
        'username': token.user.username,
        'first_name': token.user.first_name,
        'last_name': token.user.last_name,
        'email': token.user.email,
        'email_verified': email_verified
    }

    return JsonResponse(dic, status=200)
