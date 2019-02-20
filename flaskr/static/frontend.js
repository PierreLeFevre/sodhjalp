$(window).on("load", function(){
	
});

function showHideComments(element){
	var toggle = $(element).parent().parent().find('.comments-box').fadeToggle('fast');
	
	var element = $(element);
	var text = element.text();

	
	if (text == "Dölj kommentarer"){
		element.text("Visa kommentarer");
	}
	else if (text == "Visa kommentarer"){
		element.text("Dölj kommentarer");
	}
}