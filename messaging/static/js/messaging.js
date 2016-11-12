
function messaging_confirm_read(message_ids, success_call_back){
    $.ajax({
        url: get_url('messaging_confirm_read'),
        type: 'POST',
        data: {
            message_ids: message_ids,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        console.log(msg)
        if (msg['success'] == true) {
            success_call_back()
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}