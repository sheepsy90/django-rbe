
function updateLocation(position) {
    $.ajax({
        method: 'POST',
        url: get_url('profile_update_location'),
        data: {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            window.location.reload();
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}

function clear_location() {
    $.ajax({
        method: 'POST',
        url: get_url('profile_clear_location'),
        data: {
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
           window.location.reload();
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}