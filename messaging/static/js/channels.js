/**
 * Created by rkessler on 2017-01-31.
 */

function connect_socket(protocol, uri, port, onopen) {
    var socket = new ReconnectingWebSocket(protocol + "://" + window.location.host + ':' + port + uri);
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

    // Bind a new message handler
    socket_wrapper.on = function(type, _function){
        message_handlers[type] = _function;
    };
    socket_wrapper.send = function(payload){
        socket.send(JSON.stringify(payload));
    };
    return socket_wrapper;
}