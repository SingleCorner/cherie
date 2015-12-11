$(document).ready(function() {

	if ($('li').hasClass('active')) {
		$('li').removeClass('active');
	}
});


function navbar_ajust() {
	if ($(document).scrollTop() > 60) {
		if (!$('body').hasClass('scroll')){
			$('body').addClass('scroll');
		}
	} else {
		$('body').removeClass('scroll');
	}
}