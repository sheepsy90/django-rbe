import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from library.log import rbe_logger


@channel_session_user_from_http
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})

    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")

    # Save room in session and add us to the group
    message.channel_session['room'] = room
    group = Group("chat-%s" % room)
    group.add(message.reply_channel)
    group.send({
        "text": json.dumps({
            'type': 'user_joined',
            'user': message.user.username
        })
    })


@channel_session_user
def ws_message(message):
    try:
        payload = json.loads(message['text'])
        room = message.content['path'].strip("/")

        if payload.get('type', None) == 'message':
            Group("chat-%s" % room).send({
                "text": json.dumps({
                    'type': 'message_received',
                    'user': message.user.username,
                    'message': payload.get('message')
                })
            })
        if payload.get('type', None) == 'ping':
            message.reply_channel.send({
                "text": json.dumps({
                    'type': 'pong'
                })
            })

    except Exception as e:
        print "Exception"
        rbe_logger.exception(e)

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    room = message.content['path'].strip("/")

    Group("chat-%s" % room).send({
        "text": json.dumps({
            'type': 'user_joined',
            'user': message.user.username
        })
    })

    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)