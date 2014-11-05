function update_knob(element, data) {
  if($('.done_onoffswitch-checkbox', element).prop("checked")) {
    $(".done_onoffswitch-switch", element).css("background-image", "url("+data['checked']+")");
    $(".done_onoffswitch-switch", element).css("background-color", "#018801;");
  } else {
    $(".done_onoffswitch-switch", element).css("background-image", "url("+data['unchecked']+")");
    $(".done_onoffswitch-switch", element).css("background-color", "#FFFFFF;");
  }
}

function DoneXBlock(runtime, element, data) {
    $('.done_onoffswitch-checkbox', element).prop("checked", data.state);
    update_knob(element, data);
    var handlerUrl = runtime.handlerUrl(element, 'toggle_button');

    function updateCount(result) {}

    $(function ($) {
	// Don't have animations on for above class changes. This is probably not necessary. I 
	// was seeing animations on page load. I did a few things to fix it. The line below 
	// wasn't the one that fixed it, but I decided to keep it anyways. 
	//$('.done_block', element).addClass("done_windshield_animated");
	$('.done_onoffswitch', element).addClass("done_animated");
	$('.done_onoffswitch-checkbox', element).change(function(){
	    $.ajax({
		type: "POST",
		url: handlerUrl,
		data: JSON.stringify({"done":$('.done_onoffswitch-checkbox', element).prop("checked")}),
		success: updateCount
	    });
	    update_knob(element, data);
	});
    });
}
