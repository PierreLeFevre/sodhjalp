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

function livePreviewCreate(){
	var title = $(".live-input-title").val();
	var body = $(".live-input-body").val();
	var topic = $(".live-input-topic").val();
	var date = new Date;
	var time = date.now;

	console.log("hej");

	//setting values

	$(".live-preview-title").text(title);
	$(".live-preview-body").text(body);
	$(".live-preview-topic").text(topic);

}

$(window).on("load", function(){
	var url_for_search = $("#search").parent().attr("action");

	$("#search").on("input", function(){
		$(this).parent().attr("action", (url_for_search + $(this).val()));
	});

	$(".post-clickable-pills").on("click", function(){
		window.location.replace("/search/" + $(this).text());
	});

	$(".shadow-hover").on("mouseover", function(){
		if ($(this).hasClass("shadow")){
			$(this).removeClass("shadow").addClass("shadow-lg");
		} else {
			$(this).addClass("shadow");			
		}
	});

	$(".shadow-hover").on("mouseout", function(){
		if ($(this).hasClass("shadow-lg")){
			$(this).removeClass("shadow-lg").addClass("shadow");
		} else {
			$(this).removeClass("shadow").addClass("shadow-lg");			
		}
	});

	$(".live-input-body").on("input", function(){
		livePreviewCreate()
	});

	$(".live-input-topic").on("input", function(){
		livePreviewCreate()
	});

	$(".live-input-title").on("input", function(){
		livePreviewCreate()
	});


});















