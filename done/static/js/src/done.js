function DoneXBlock(runtime, element) {

    function updateCount(result) {
        console.log("Success");
    }

    var handlerUrl = runtime.handlerUrl(element, 'toggle_button');

    $('p', element).click(function(eventObject) {
    });

    $(function ($) {
	if (done_done) {
	    $('.windshield').addClass("windshield_off").removeClass("windshield_on");
	} else {
	    $('.windshield').addClass("windshield_on").removeClass("windshield_off");
	}
	// Don't have animations on for above class changes. This is probably not necessary. I 
	// was seeing animations on page load. I did a few things to fix it. The line below 
	// wasn't the one that fixed it, but I decided to keep it anyways. 
	$('.windshield').addClass("windshield_animated")
	$('.windshield').click(function(){
            $(this).toggleClass("windshield_on");
            $(this).toggleClass("windshield_off");
	    $.ajax({
		type: "POST",
		url: handlerUrl,
		data: JSON.stringify({"done":$(this).hasClass("windshield_off")}),
		success: updateCount
          
	    });
	});
    });
}
