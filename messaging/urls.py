from django.conf.urls import url

import messaging.views


urlpatterns = [
    url(r'inbox', messaging.views.inbox, name="inbox"),
    url(r'outbox', messaging.views.outbox, name="outbox"),
    url(r'messages', messaging.views.messages, name='messages'),
    url(r'message/(?P<message_id>\d*)$', messaging.views.message, name='message'),
    url(r'delete$', messaging.views.delete_message, name='message-delete'),
    url(r'compose/(?P<recipient_user_id>\d*)$', messaging.views.compose, name='compose'),
    url(r'conversation/(?P<user_id>\d*)$', messaging.views.conversation, name='conversation'),
    url(r'send$', messaging.views.send, name='send'),
    url(r'messaging_confirm_read', messaging.views.messaging_confirm_read, name='messaging_confirm_read'),
]
