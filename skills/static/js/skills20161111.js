/**
 * Created by rkessler on 2016-10-30.
 */

function create_skill(level, skill_name, call_back_object_create_on_success) {
    $.ajax({
        method: 'POST',
        url: get_url('create_skill'),
        data: {
            level: level,
            skill_name: skill_name,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            call_back_object_create_on_success(msg)
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}

function change_skill_level_local($element, delta){
    var v = parseInt($element.html());
    v += delta;
    if (v < 1){v = 1}
    if (v > 5){v = 5}
    $element.html(v)
}


function increase_skill(skill_id, $target){
    $.ajax({
        method: 'POST',
        url: get_url('up_skill_level'),
        data: {
            skill_id: skill_id,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            $target.html(msg['new_level']);
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}

function decrease_skill(skill_id, $target){
    $.ajax({
        method: 'POST',
        url: get_url('down_skill_level'),
        data: {
            skill_id: skill_id,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            $target.html(msg['new_level']);
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}

function remove_skill(skill_id, $target){
  $.ajax({
        method: 'POST',
        url: get_url('delete_skill'),
        data: {
            skill_id: skill_id,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            $target.remove();
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}

function forward_skill(event){
    var phrase_id = $(event.currentTarget).data('phrase-id');
    window.location.href = get_url('phrase_details') + phrase_id
}

function skill_find_matching(search_term, response_display_callback){
    $.ajax({
        method: 'POST',
        url: get_url('search_skill'),
        data: {
            search_term: search_term,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            response_display_callback(msg['skills']);
        }
    }).fail(function () {
        return swal('Error', 'Could not reach server!', 'error');
    });
}