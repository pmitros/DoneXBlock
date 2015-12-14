/* Dummy code to make sure events work in Workbench as well as
 * edx-platform*/
if (typeof Logger === 'undefined') {
    var Logger = {
        log: function(a, b) { return; }
    };
}

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

    if (data.align != "right") {
	$('.done_right_spacer', element).addClass("done_grow");
    }
    if (data.align != "left") {
	$('.done_left_spacer', element).addClass("done_grow");
    }

    update_knob(element, data);
    var handlerUrl = runtime.handlerUrl(element, 'toggle_button');

    $(function ($) {
	$('.done_onoffswitch', element).addClass("done_animated");
	$('.done_onoffswitch-checkbox', element).change(function(){
	    var checked = $('.done_onoffswitch-checkbox', element).prop("checked");
	    $.ajax({
		type: "POST",
		url: handlerUrl,
		data: JSON.stringify({'done':checked})
	    });
	    Logger.log("edx.done.toggled", {'done': checked});
	    update_knob(element, data);
	});
    });
}
