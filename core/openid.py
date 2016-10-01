
def user_info(STANDARD_CLAIMS, user):
    print STANDARD_CLAIMS, user
    return {}

from django.utils.translation import ugettext as _
from oidc_provider.lib.claims import ScopeClaims

class CustomScopeClaims(ScopeClaims):

    info_tags = (
        _(u'Tags'),
        _(u'The tags you entered in the self description'),
    )

    info_location = (
        _(u'Location'),
        _(u'Some location for the scope.'),
    )

    def scope_location(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        dic = {
            'location': 'Something location here',
        }

        return dic

    def scope_foo(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        dic = {
            'bar': 'Something dynamic here',
        }

        return dic

    # If you want to change the description of the profile scope, you can redefine it.
    info_profile = (
        _(u'Profile'),
        _(u'Another description.'),
    )
