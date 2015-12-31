$(document).ready(function() {

	if ($('li').hasClass('active')) {
		$('li').removeClass('active');
	}
	
	pathname = window.location.pathname;
	module = pathname.split('/')[2];
	id = pathname.split('/')[3];
	$('#nav-' + module).addClass('active');
	$('#subnav-' + id).addClass('active');

	$('#createGroup_submit').submit(addGroup);

});


function addGroup(evt) {
	evt.preventDefault();
	var group_name = $('#createGroup_name').val();
	$.ajax({
		type: 'POST',
		url: '/exec',
		data: {
			'module': "group",
			'action': "create",
			'addGroup_name': group_name,
		},
		timeout: 5000,
		success: function(data, status, xhr) {
			if (data.code == 0) {
				$('#createGroup_info').html(data.message);
				setTimeout(function(){
						window.location.reload();
					},1500
				);					
			}
		},
		error: function(data) {
		},
		dataType: 'json'
	});
}

