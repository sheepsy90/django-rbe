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
            $(event.currentTarget).hide(500).remove();
        }
    });
}

function create_language_button(lang, language_display){
    var r1 = $('<div class="lang_button btn btn-default" data-lang="' + lang + '">');
    var c1 = $('<img style="height: 2em; margin-top: -6px" src="/static/img/language_flags/' + lang + '.png" alt=""/>');
    var c2 = $('<span style="font-size: 20px; height: 2em">' + language_display + '</span>');
    var c3 = $('<span class="fa fa-remove" style="font-size: 15px;"></span>');
    $(r1).append(c1)
    $(r1).append(c2)
    $(r1).append(c3)
    return r1;
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
            $target_container.append(btn);
        }
    });
}

function forward_language(event){
    var lang = $(event.currentTarget).data('lang');
    window.location.href = get_url('language_overview') + lang
}