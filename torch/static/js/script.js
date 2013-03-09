$(document).ready(function() {
	$('.idea-info').height($('.count-action').height());
	$(window).resize(function() {
		$('.idea-info').height($('.count-action').height());
	});
	
	enableSubmitForm();
});

function enableSubmitForm() {
	$('.slideshow').cycle({
		timeout: 0,
		next: '.slide-next',
		prev: '.slide-back',
		fx: 'scrollHorz',
	});
}