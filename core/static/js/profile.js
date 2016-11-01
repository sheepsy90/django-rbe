function upload_profile_image(event) {
    event.preventDefault();
    var files = event.target.files;

    if (files.length != 1) {
        return swal('Error', 'You can only select one image!', 'error');
    }

    var data = new FormData();
    $.each([files[0]], function (key, value) {
        data.append(key, value);
    });

    data.append('csrfmiddlewaretoken', get_csrf_token());

    $.ajax({
        url: get_url('profile_avatar_upload'),
        type: 'POST',
        data: data,
        cache: false,
        dataType: 'json',
        processData: false, // Don't process the files
        contentType: false // Set content type to false as jQuery will tell the server its a query string request
    }).done(function (msg) {
        if (msg['success'] == true) {
            var path = msg['path'];
            $('#user-picture').attr('src', path);
        } else {
            return swal('Error', 'Could not upload your profile picture!', 'error');
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}


function updateLocation(position) {
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
            window.location.reload();
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}

function clear_location() {
    $.ajax({
        method: 'POST',
        url: get_url('clear_location'),
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