$(document).ready(function () {
		$('#btn1').show(); 
        $('#btn2').hide();
        $('#btn3').hide();
        $('#btn4').hide();
		
		$("#menubtn1").addClass("sel");
        });
		
$(document).ready(function () {
    $('#menubtn1').click(function () {
        $('#btn2').hide();
        $('#btn3').hide();
        $('#btn4').hide();
        $('#btn1').show(); 
		
		$("#menubtn1").addClass("sel");
		$("#menubtn2").removeClass("sel");
		$("#menubtn3").removeClass("sel");
		$("#menubtn4").removeClass("sel");
		
    });
});

$(document).ready(function () {
    $('#menubtn2').click(function () {
        $('#btn1').hide();
        $('#btn3').hide();
        $('#btn4').hide();
        $('#btn2').show(); 
		
		$("#menubtn1").removeClass("sel");
		$("#menubtn2").addClass("sel");
		$("#menubtn3").removeClass("sel");
		$("#menubtn4").removeClass("sel");
    });
});

$(document).ready(function () {
    $('#menubtn3').click(function () {
        $('#btn1').hide();
        $('#btn2').hide();
        $('#btn4').hide();
        $('#btn3').show(); 
		
		$("#menubtn1").removeClass("sel");
		$("#menubtn2").removeClass("sel");
		$("#menubtn3").addClass("sel");
		$("#menubtn4").removeClass("sel");
    });
});

$(document).ready(function () {
    $('#menubtn4').click(function () {
        $('#btn1').hide();
        $('#btn2').hide();
        $('#btn3').hide();
        $('#btn4').show(); 
		
		$("#menubtn1").removeClass("sel");
		$("#menubtn2").removeClass("sel");
		$("#menubtn3").removeClass("sel");
		$("#menubtn4").addClass("sel");
    });
});