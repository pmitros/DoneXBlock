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
    $(".emojis_reaction",element).css("display","block");
  } else {
    $(".emojis_reaction",element).css("display","none")
    $(".done_onoffswitch-switch", element).css("background-image", "url("+data['unchecked']+")");
    $(".done_onoffswitch-switch", element).css("background-color", "#FFFFFF;");
  }
}

function DoneXBlock(runtime, element, data) {
    $('.done_onoffswitch-checkbox', element).prop("checked", data.state);
    update_knob(element, data);
    var handlerUrl = runtime.handlerUrl(element, 'toggle_button');
    var handlerUrlEmoji = runtime.handlerUrl(element, 'react_emoji');
    updateReaction(data.selected,element,handlerUrlEmoji)


    $('.emoji',element).click(function(e){
       
      updateReaction(e.currentTarget.id,element,handlerUrlEmoji)
    })
    if(data.state && !data.unmarking){
      $('.done_onoffswitch-checkbox', element)[0].disabled=true;
      return;
    } 
  $(function ($) {
	$('.done_onoffswitch', element).addClass("done_animated");
	$('.done_onoffswitch-checkbox', element).change(function(){
	    var checked = $('.done_onoffswitch-checkbox', element).prop("checked");

      if( !data.unmarking){
        $('.done_onoffswitch-checkbox', element)[0].disabled=true;
      }
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

 reactions.forEach(reactState=>{
  if(reactState!==react){
   $("#"+reactState,element).addClass('emoji_unselected')
  }
})
if (react==='none') return;


  $("#"+react,element).addClass("react_animated");
  $("#"+react,element).removeClass("emoji_unselected");

 $("#"+react,element).css("font-size","20px")

  $.ajax({
		type: "POST",
		url: url,
		data: JSON.stringify({'selected':react})
	    });


}