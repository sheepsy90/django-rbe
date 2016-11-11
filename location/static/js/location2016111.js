
function updateLocation(position, success_callback) {
    $.ajax({
        method: 'POST',
        url: get_url('update_location'),
        data: {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            success_callback()
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}

function clear_location(success_handler) {
    $.ajax({
        method: 'POST',
        url: get_url('clear_location'),
        data: {
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            success_handler()
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}