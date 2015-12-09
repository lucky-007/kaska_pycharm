var ajax_timeout = 2000;
var interval = null;

function check_teams() {
    var $ =jQuery;
    var req_teams_available = $.ajax({
        method: 'GET',
        url: 'http://kaska.me/teams/available/',
        data: {pool: $('#ajax_data').text()},
        dataType: 'json',
        timeout: ajax_timeout
    });

    req_teams_available.done(function (msg) {
        for(var t in msg){
            $('#but'+t).prop('disabled', (msg[t] != true));
        }
    }).fail(function (jqXHR, textStatus) {
        if (textStatus == 'timeout') {
            alert('Timeout error');
        }
    });
}

function get_part_of_html($){
    return $.ajax({
        method: 'GET',
        url: 'http://kaska.me/teams/success/',
        dataType: 'html',
        async: false,
        error: function(){
            alert('Request failed');
        }
    }).responseText;
}

(function($){
    $(document).ready(function(){
        var $submit_btn = $('input[type=submit]');

        $('button.team_button').click(function(){
            $('button.team_button').each(function(){
                $(this).removeClass('selected');
            });
            $(this).addClass('selected');
            $('#ajax_errors').hide('fast');
            $('#team_submit').val(this.id.substring(3));
            $submit_btn.prop('disabled', false);
        });

        var form = $('form');
        form.submit(function(){
            $submit_btn.prop('disabled', true);
            $.ajax({
                method: form.attr('method'),
                url: form.attr('action'),
                data: form.serialize(),
                dataType: 'json',
                success: function(msg){
                    if('error' in msg){
                        $('#ajax_errors').html(msg['error']).show("slow");
                        $submit_btn.prop('disable', true);
                    } else {
                        $('#team_selection_page').hide().html(get_part_of_html(jQuery)).show("fast");
                        clearInterval(interval);
                    }
                },
                error: function(){
                    alert('Request failed');
                }

            });
            return false;
        });

        $(document).ajaxSend(function(){
            $('#loading').show();
        });
        $(document).ajaxComplete(function(){
            $('#loading').hide();
        });

        if($('form').length) {
            check_teams();
            interval = setInterval(check_teams, ajax_timeout);
        }
    });
})(jQuery);