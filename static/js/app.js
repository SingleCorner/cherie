$(document).ready(function() {

	if ($('li').hasClass('active')) {
		$('li').removeClass('active');
	}
	
	pathname = window.location.pathname;
	module = pathname.split('/')[2];
	id = pathname.split('/')[3];
	$('#' + module).addClass('active');
	$('#subnav-' + id).addClass('active');
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