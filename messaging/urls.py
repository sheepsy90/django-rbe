from django.conf.urls import url

import messaging.views


urlpatterns = [
    url(r'messages', messaging.views.messages, name='messages'),
    url(r'conversation/(?P<user_id>\d*)$', messaging.views.conversation, name='conversation'),
    url(r'send$', messaging.views.send, name='send'),
    url(r'messaging_confirm_read', messaging.views.messaging_confirm_read, name='messaging_confirm_read'),
    url(r'chat', messaging.views.chat, name='chat'),
]
