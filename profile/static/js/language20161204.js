/**
 * Created by rkessler on 2016-10-29.
 */
function remove_language(event){
    console.log("Remove language");

    var lang = $(event.currentTarget).data('lang');

    console.log(lang);
    $.ajax({
        method: 'POST',
        url: get_url('language_remove'),
        data: {
            lang: lang,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            $(event.currentTarget).parent().hide(500).remove();
        }
    });
}

function change_lang_skill(lang_code, new_value, success_callback) {
    $.ajax({
        method: 'POST',
        url: get_url('language_level_change'),
        data: {
            lang_code: lang_code,
            new_value: new_value,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            success_callback();
        }
    });
}

function increase_lang_skill(){
    var $active = $(this).parent().find('.lang-level.active');
    var $next = $active.next();
    var lang_code = $(this).parent().find('input').data('lang');

    if ($next.length != 0){
        change_lang_skill(lang_code, $next.data('value'), function(){
            $active.removeClass('active');
            $next.addClass('active');
        });
    }
}

function decrease_lang_skill(){
    var $active = $(this).parent().find('.lang-level.active');
    var $prev = $active.prev();
    var lang_code = $(this).parent().find('input').data('lang');

    if ($prev.length != 0){
        change_lang_skill(lang_code, $prev.data('value'), function(){
            $active.removeClass('active');
            $prev.addClass('active');
        });
    }
}

function create_language_button(lang, language_display){
    var element = $('.blueprint').find(".language_display").clone();
    $(element).removeClass('language_display');

    $(element).find('#language_display').val(language_display);
    $(element).find('#language_display').data('lang', lang);
    $(element).find('#language_display').click(forward_language);

    var href = $(element).find('#flag_img').attr('src');
    $(element).find('#flag_img').attr('src', href + lang + '.png');

    $(element).find('.lang_remove').data('lang', lang);
    $(element).find('.lang_remove').click(remove_language);

    $(element).find('.increase-language-skill').click(increase_lang_skill);
    $(element).find('.decrease-language-skill').click(decrease_lang_skill);

    return element;
}



function add_language($select_box, $target_container){
    var lang = $select_box.find(":selected").val();
    $.ajax({
        method: 'POST',
        url: get_url('language_add'),
        data: {
            lang: lang,
            csrfmiddlewaretoken: get_csrf_token()
        }
    }).done(function (msg) {
        if (msg['success']) {
            var btn = create_language_button(lang, msg['language_display']);
            $target_container.prepend(btn);
        }
    });
}

function forward_language(event){
    var lang = $(event.currentTarget).data('lang');
    window.location.href = get_url('language_overview') + lang
}