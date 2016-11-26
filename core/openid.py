from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from oidc_provider.lib.claims import ScopeClaims

class CustomScopeClaims(ScopeClaims):

    info_identity = (
        _('Identity'),
        _('The application gets access to your identity including email_address, user_id, and username.'),
    )

    info_location = (
        _('Location'),
        _('The application gets access to read your location.'),
    )

    info_skills = (
        _('Skills'),
        _('The application gets access to read your skills.'),
    )

    info_languages = (
        _('Languages'),
        _('The application gets access to read your languages.'),
    )