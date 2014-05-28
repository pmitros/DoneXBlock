function DoneXBlock(runtime, element) {

    function updateCount(result) {
        console.log("Success");
    }

    var handlerUrl = runtime.handlerUrl(element, 'toggle_button');

    $('p', element).click(function(eventObject) {
    });

    $(function ($) {
	$('.windshield').click(function(){
            $(this).toggleClass("windshield_on");
            $(this).toggleClass("windshield_off");
	    console.log($(this).hasClass("windshield_on"));
	    $.ajax({
		type: "POST",
		url: handlerUrl,
		data: JSON.stringify({"hello": "world"}),
		success: updateCount
          
	    });
	});
    });
}
