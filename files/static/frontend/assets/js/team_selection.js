var ajax_timeout = 3000;
var interval = null;

function check_teams() {
    var $ =jQuery;
    var req_teams_available = $.ajax({
        method: 'GET',
        //url: 'http://kaska.me/teams/available/',
        url: 'http://127.0.0.1:8000/teams/available/',
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

(function($){
    $(document).ready(function(){
        var $submit_btn = $('input[type=submit]');

        $('button.team_button').click(function(){
            $('button.team_button').each(function(){
                $(this).removeClass('selected');
            });
            $(this).addClass('selected');
            $('#ajax_errors').hide('fast');
            $('#team_submit').val(this.id[3]);
            $submit_btn.prop('disabled', false);
        });

        var form = $('form');
        form.submit(function(event){
            $submit_btn.prop('disabled', true);
            $.ajax({
                method: form.attr('method'),
                url: form.attr('action'),
                data: form.serialize(),
                dataType: 'json',
                success: function (msg) {
                    if('error' in msg){
                        $('#ajax_errors').html(msg['error']).show("slow");
                        $submit_btn.prop('disable', true);
                    } else {
                        $('#team_selection_page').html('<b>Thanks for selecting</b>');
                        clearInterval(interval);
                    }
                },
                error: function (msg) {
                    alert('Request failed');
                }

            });
            return false;
        });

        $(document).ajaxSend(function(event, request, settings){
            $('#loading').show();
        });
        $(document).ajaxComplete(function(event, request, settings){
            $('#loading').hide();
        });

        check_teams();
        interval = setInterval(check_teams, ajax_timeout);
    });
})(jQuery);