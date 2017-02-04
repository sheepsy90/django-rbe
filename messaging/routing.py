# In routing.py
from channels.routing import route, include

import messaging.consumers as consumers

channel_routing = [
    route("websocket.connect", consumers.ws_connect, path=r"^/chat/$"),
    route("websocket.receive", consumers.ws_message, path=r"^/chat/$"),
    route("websocket.disconnect", consumers.ws_disconnect, path=r"^/chat/$"),
]
