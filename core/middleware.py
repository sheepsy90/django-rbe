import datetime
import time

from django.conf import settings
from django.contrib import auth

from core.models import LastSeen


class LastSeenMiddleware(object):

    def process_request(self, request):
        """ Update the last seen time """
        if request.user.is_authenticated():
            ls, created = LastSeen.objects.get_or_create(user=request.user)
            ls.date_time = datetime.datetime.now()
            ls.save()


class AutoLogout(object):

    def process_request(self, request):
        # Cannot logout if no user is there
        if not hasattr(request, 'user'):
            return

        # Cannot logout if not logged in
        if not request.user.is_authenticated():
            return

        try:
            if time.time() - request.session['last_touch'] > settings.AUTO_LOGOUT_DELAY:
                auth.logout(request)
                del request.session['last_touch']
                return
        except KeyError:
            pass

        request.session['last_touch'] = time.time()