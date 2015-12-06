function check_teams() {
    var $ =jQuery;
    var request = $.ajax({
        method: 'GET',
        //url: 'http://kaska.me/teams/available/',
        url: 'http://127.0.0.1:8000/teams/available/',
        data: {pool: $('p[hidden]').text()},
        dataType: 'json',
        timeout: 3000
    });

    request.done(function (msg) {
        for(var t in msg){
            $('#but'+t).prop('disabled', (msg[t] != true));
        }
    }).fail(function (jqXHR, textStatus) {
        if (textStatus == 'timeout') {
            alert('timeout error');
        }
    });
}

setInterval(check_teams, 3000);

(function($){
    $(document).ready(function(){
        $('button.team_button').click(function(){
            $('button.team_button').each(function(){
                $(this).removeClass('selected');
            });
            $(this).addClass('selected');
            $('#team_submit').val(this.id[3]);
            $('input[type=submit]').prop('disabled', false);
        });
    });

    check_teams();

})(jQuery);