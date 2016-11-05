import datetime

from core.models import LastSeen


class LastSeenMiddleware(object):

    def process_request(self, request):
        """ Update the last seen time """
        if request.user.is_authenticated():
            ls, created = LastSeen.objects.get_or_create(user=request.user)
            ls.date_time = datetime.datetime.now()
            ls.save()
