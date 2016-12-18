import uuid

from django.utils import timezone
from oidc_provider.models import Client, Token


def create_api_preconditions_with_scope(user, scopes):
    assert isinstance(scopes, list)
    bearer = uuid.uuid4().hex

    client = Client(name='test_client')
    client.save()

    expires_at = timezone.now() + timezone.timedelta(days=30)
    t = Token(scope=scopes, access_token=bearer, user=user, expires_at=expires_at, client=client)
    t.save()

    return bearer