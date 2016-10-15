from django.conf.urls import url

import messaging.views


urlpatterns = [
    url(r'inbox', messaging.views.inbox, name="inbox"),
    url(r'outbox', messaging.views.outbox, name="outbox"),
    url(r'message/(?P<message_id>\d*)$', messaging.views.message, name='message'),
    url(r'delete$', messaging.views.delete_message, name='message-delete'),
    url(r'compose/(?P<recipient_user_id>\d*)$', messaging.views.compose, name='compose'),
]