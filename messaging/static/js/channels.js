/**
 * Created by rkessler on 2017-01-31.
 */

function connect_socket(uri, onopen) {
    var socket = new WebSocket("ws://" + window.location.host + uri);
    var message_handlers = {};

    socket.onopen = function() {
        // Initial message
        if (onopen) {
            onopen(socket);
        }
    };

    // Call onopen directly if socket is already open
    if (socket.readyState == WebSocket.OPEN) socket.onopen();

    socket.onmessage = function(e) {

        // Parse server message from JSON
        try {
            var server_content = JSON.parse(e.data);
            var handler = message_handlers[server_content.type];
            handler(server_content);
        } catch (err) {

        }
    };

    var socket_wrapper = {};
    socket_wrapper.socket = socket;
    socket_wrapper.message_handlers = message_handlers;
    return socket_wrapper;
}