import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from django.utils import timezone
from library.log import rbe_logger
from messaging.models import ChatMessage


@channel_session_user_from_http
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})

    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")

    cm_qs = ChatMessage.objects.all().order_by('-sent_time')[:30]

    # Send the client all old messages
    x = [cm.as_payload for cm in cm_qs]
    x.reverse()
    [message.reply_channel.send(t) for t in x]

    # Save room in session and add us to the group
    message.channel_session['room'] = room
    group = Group("chat-%s" % room)
    group.add(message.reply_channel)
    group.send({
        "text": json.dumps({
            'type': 'user_joined',
            'time': timezone.now().strftime('%Y-%m-%d %H:%M %Z'),
            'user': message.user.username
        })
    })


@channel_session_user
def ws_message(message):
    try:
        payload = json.loads(message['text'])
        room = message.content['path'].strip("/")

        if payload.get('type', None) == 'message':
            cm = ChatMessage(author=message.user, message=payload.get('message'), sent_time=timezone.now())
            cm.save()

            Group("chat-%s" % room).send(cm.as_payload)

    except Exception as e:
        print "Exception"
        rbe_logger.exception(e)

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    try:
        room = message.content['path'].strip("/")

        Group("chat-%s" % room).send({
            "text": json.dumps({
                'type': 'user_left',
                'time': timezone.now().strftime('%Y-%m-%d %H:%M %Z'),
                'user': message.user.username
            })
        })

        Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
    except Exception as e:
        rbe_logger.exception(e)