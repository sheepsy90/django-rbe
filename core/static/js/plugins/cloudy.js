/**
 * @depends
 *  - get_csrf_token()
 *  - jqcloud.html import
 *
 * @resources
 *  - cloudy.scss
 *  - cloudy.html
 *
 * @specification
 * root_element - The div in which the element should be manifest
 * tag_receive_url - The url where to get the tag data and the filtered results from
 * generate_element - A function taking the server response per element and returns a dom element
 *
 * The ajax request needs to return:
 * objects - list - the list of all the available objects  for those tags
 * success - indicates if the request was processed correctly true
 * tags - dictionary - a key value structure with tags and the occurrence count of the respective tags
 */

function bind_cloud_area(root_element, tag_receive_url, generate_element){

    // Check if the html element is there that is the basis for cloning
    if ($("#cloudy_mixin_templates").length == 0){
        console.error("Cloudy mixin is missing - please include it!");
        return
    }

    var update_filter = function(){
        var arr = jQuery.map($(root_element).find("#tags_selected > h3 > .realtag"), function (a) {
            return $(a).html();
        });

        var initial = false;
        if (arr.length == 0) {
            initial = true;
        }

        $.ajax({
            method: "POST",
            url: tag_receive_url,
            data: {
                chosen_tags: arr.join(),
                csrfmiddlewaretoken: get_csrf_token()
            }
        }).done(function (msg) {
            var tags = new Array();
            for (var e in msg['tags']) {
                tags.push({
                    text: '' + e,
                    weight: '' + msg['tags'][e],
                    handlers: {
                        click: function (e) {
                            var element = e.currentTarget;
                            clicked_tag($(element).html());
                        }
                    }
                });
            }

            if (initial) {
                try {
                    $(root_element).find('#tag_cloud').jQCloud('destroy');
                } catch (err) {}
                $(root_element).find('#tag_cloud').jQCloud(tags, {
                        delayedMode: true
                    }
                );
            } else {
                if (tags.length > 0) {
                    $(root_element).find('#tag_cloud').jQCloud('update', tags);
                } else {
                    $(root_element).find('#tag_cloud').jQCloud('destroy');
                }
            }

            update_filter_box(msg['objects']);
        }).fail(function(){
            console.error("Something went wrong with contacting the server")
        });
    };



    var update_filter_box = function(objects) {
        $(root_element).find('#filtered').empty();
        for (var e in objects) {
            var element = generate_element(objects[e]);
            $(root_element).find("#filtered").append(element);
        }
    };


    var clicked_tag = function(tag){
        var f = $('<h3><span class="label label-success realtag">' + tag + '</span></h3>');
        $(f).addClass('selected_tag');
        $(root_element).find('#tags_selected').append(f);
        $(f).click(function () {
            $(f).remove();
            update_filter();
        });
        update_filter();
    };


    var stuff = $("#cloudy_mixin_templates").find('#cloudy-part').clone();

    $(stuff).attr('id', 'cloudy').show();
    $(root_element).empty().append(stuff);


       // Searching and removing filter tags
    $(root_element).find("#search_for_tag").keypress(function(e){
        if(e.which == 13) {
            e.preventDefault();
            var value = $(root_element).find("#search_for_tag").html();
            clicked_tag(value);
            $(root_element).find("#search_for_tag").html('');
        }
    });

    $(root_element).find("#search_for_tag").click(function(e){
        $(root_element).find("#search_for_tag").html('');
    });

    $(root_element).find("#clear_selected_tags").click(function(){
        $(root_element).find("#tags_selected > h3 > .realtag").parent().remove();
        update_filter();
    });


    $(root_element).data({
       clear: function(){
           $(root_element).find("#clear_selected_tags").click();
       }
    });
}






