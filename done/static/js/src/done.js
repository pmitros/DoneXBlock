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
    console.log("eeee",data)
    $(".emojis_reaction",element).css("display","block");
  } else {
    $(".emojis_reaction",element).css("display","none")
    $(".done_onoffswitch-switch", element).css("background-image", "url("+data['unchecked']+")");
    $(".done_onoffswitch-switch", element).css("background-color", "#FFFFFF;");
  }
}

function DoneXBlock(runtime, element, data) {
  console.log("elem",element)
    $('.done_onoffswitch-checkbox', element).prop("checked", data.state);

    update_knob(element, data);
    var handlerUrl = runtime.handlerUrl(element, 'toggle_button');
    var handlerUrlEmoji = runtime.handlerUrl(element, 'react_emoji');

    console.log("hanldeYr",handlerUrl)

    $('.emoji',element).click(function(e){
       
      console.log(e.currentTarget.id);
      updateReaction(e.currentTarget.id,element,handlerUrlEmoji)
    })
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

function updateReaction(react,element,url){
 reactions = ['confused','love','like'];
  $("#"+react,element).addClass("react_animated");
 $("#"+react,element).css("font-size","20px")

 reactions.forEach(reactState=>{
   if(reactState!==react){
    $("#"+reactState,element).css("font-size","14px")
   }
 })
  $.ajax({
		type: "POST",
		url: url,
		data: JSON.stringify({'selected':react})
	    });


}