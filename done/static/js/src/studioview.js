
function Toggle_Unmarking(runtime,element,data){
    $('#enabled_'+data.id,element)[0].checked=data.unmarking
   var url= runtime.handlerUrl(element, 'toggle_unmarking');
 $('input',element).click(function(e){
    $.ajax({
		type: "POST",
		url: url,
		data: JSON.stringify({'unmarking':e.currentTarget.value=='disabeled'?false:true})
	    });

 })
}