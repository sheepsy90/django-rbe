/**
 * Created by rkessler on 2016-10-29.
 */

function load_chart_data(element_id){
    function drawChart() {
        $.ajax({
            method: 'POST',
            url: get_url('language_chart'),
            data: {
                csrfmiddlewaretoken: get_csrf_token()
            }
        }).done(function (msg) {
            if (msg['success']) {
                var data = google.visualization.arrayToDataTable(msg['language_count']);
                var options = {
                  title: 'Languages available in the network'
                };

                var chart = new google.visualization.PieChart(document.getElementById(element_id));
                chart.draw(data, options);
            }
        });
      }
    return drawChart;
}

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

function create_language_button(lang, language_display){
    var element = $('.blueprint').find(".language_display").clone();
    $(element).removeClass('language_display');

    $(element).find('#language_display').val(language_display);
    $(element).find('#language_display').data('lang', lang);
    $(element).find('#language_display').click(forward_language);

    var href = $(element).find('#flag_img').attr('src');
    $(element).find('#flag_img').attr('src', href + lang + '.png');

    $(element).find('.remove_language').data('lang', lang);
    $(element).find('.remove_language').click(remove_language);

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
            $(btn).click(remove_language)
            $target_container.prepend(btn);
        }
    });
}

function forward_language(event){
    var lang = $(event.currentTarget).data('lang');
    window.location.href = get_url('language_overview') + lang
}