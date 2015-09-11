/* Dummy code to make sure events work in Workbench as well as
 * edx-platform*/
if (typeof Logger === 'undefined') {
    var Logger = {
        log: function(a, b) { return; }
    }
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

    var grow_left = 1;
    var grow_right = 1;

    if (data.align == "left") {
	grow_left = 0;
    }
    if (data.align == "right") {
	grow_right = 0;
    }

    $('.done_left_spacer', element).css("flex-grow", grow_left.toString());
    $('.done_right_spacer', element).css("flex-grow", grow_right.toString());

    update_knob(element, data);
    var handlerUrl = runtime.handlerUrl(element, 'toggle_button');

    $(function ($) {
	$('.done_onoffswitch', element).addClass("done_animated");
	$('.done_onoffswitch-checkbox', element).change(function(){
	    var checked = $('.done_onoffswitch-checkbox', element).prop("checked");
	    $.ajax({
		type: "POST",
		url: handlerUrl,
		data: JSON.stringify({'done':checked}),
	    });
	    Logger.log("edx.done.toggle", {'done': checked});
	    update_knob(element, data);
	});
    });
}
