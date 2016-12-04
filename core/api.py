from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from oidc_provider.lib.utils.oauth2 import protected_resource_view


@require_http_methods(['GET'])
@protected_resource_view(['identity'])
def identity(request, *args, **kwargs):
    """ This endpoint provides the identity of a user given a correct API token.
        :return: {'uid': <int: user_id>, 'username': <str: username>, 'email': <str: email>}
    """
    if 'token' not in kwargs:
        return HttpResponse("Provide a token", status=403)

    dic = {
        'uid': kwargs['token'].user.id,
        'username': kwargs['token'].user.username,
        'email': kwargs['token'].user.email
    }

    return JsonResponse(dic, status=200)