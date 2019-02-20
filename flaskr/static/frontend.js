Date.prototype.getWeek = function(){
					        var onejan = new Date(this.getFullYear(), 0, 1);
					        return Math.ceil((((this - onejan) / 86400000) + onejan.getDay() + 1) / 7);
					     } 

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