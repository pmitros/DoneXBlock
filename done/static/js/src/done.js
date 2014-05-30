function DoneXBlock(runtime, element) {
    var handlerUrl = runtime.handlerUrl(element, 'toggle_button');

    function updateCount(result) {}

    $(function ($) {
	if (done_done) {
	    $('.done_windshield', element).addClass("done_windshield_off").removeClass("done_windshield_on");
	} else {
	    $('.done_windshield', element).addClass("done_windshield_on").removeClass("done_windshield_off");
	}
	// Don't have animations on for above class changes. This is probably not necessary. I 
	// was seeing animations on page load. I did a few things to fix it. The line below 
	// wasn't the one that fixed it, but I decided to keep it anyways. 
	$('.done_windshield', element).addClass("done_windshield_animated")
	$('.done_windshield', element).click(function(){
            $(this).toggleClass("done_windshield_on");
            $(this).toggleClass("done_windshield_off");
	    $.ajax({
		type: "POST",
		url: handlerUrl,
		data: JSON.stringify({"done":$(this).hasClass("done_windshield_off")}),
		success: updateCount
	    });
	});
    });
}
