$(document).ready(function(){
	var selector = "a[href='" + $("p:hidden").text(); + "']";
	var link = $(selector).parent().addClass("current");
});