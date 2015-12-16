$(document).ready(function() {
	$('#USER_login').submit(function(evt) {
		// 阻断默认提交过程
		evt.preventDefault();
		
		// 准备变量
		var user = $('#USER_login_user').val();
		var pswd = $('#USER_login_pswd').val();
		var time = $('#USER_login_timestamp').val();
		
		// 检查输入
		if (user.length == 0) {
			$('#USER_login_status').html("No No No,请认真告诉我你叫什么>_< ");
			$('#USER_login_user').focus();
			return false;
		}
		
		if (pswd.length == 0) {
			$('#USER_login_status').html("密码君不见啦");
			$('#USER_login_pswd').focus();
			return false;
		}
		
		$('#USER_login_user').attr('disabled', true);
		$('#USER_login_pswd').attr('disabled', true);
		$('#USER_login_submit').attr('disabled', true);
		$('#USER_login_status').html('用力登录中，请稍等…');
		
		// 加密(2014-08-19换至新验证方式后作废)
		//pswd = $.sha1($.sha1(pswd) + time);
		
		$.ajax({
			type: 'POST',
			url: '/signin',
			data: {
				'act': "signin",
				'username': user,
				'password': pswd,
			},
			timeout: 5000,
			success: function(data, status, xhr) {
				if (data.code == 0) {
					$('#USER_login_status').html('登录成功~！系统准备ing');
					setTimeout(function(){
							window.location = data.referer || './';
						},1000
					);					
				} else {
					$('#USER_login_user').attr('disabled', false);
					$('#USER_login_pswd').attr('disabled', false);
					$('#USER_login_submit').attr('disabled', false);
					if (data.code == -1 || data.code == -2) {
						$('#USER_login_pswd').val('');
						$('#USER_login_pswd').focus();
					}
					$('#USER_login_status').html(data.message);
				}
			},
			error: function(data) {
				$('#USER_login_user').attr('disabled', false);
				$('#USER_login_pswd').attr('disabled', false);
				$('#USER_login_submit').attr('disabled', false);
				$('#USER_login_user').focus();
				$('#USER_login_pswd').val('');
				$('#USER_login_status').html(data.responseText);

			},
			dataType: 'json'
		});
	});

	// 设置焦点
	$('#USER_login_user').focus();
	//PressEnter();
});

function signup() { 
	var user = $('#USER_login_user').val();
	var pswd = $('#USER_login_pswd').val();
	alert(user);
	alert(pswd);
	$.ajax({
		type: 'POST',
		url: '/signup',
		data: {
			'act': "signup",
			'username': user,
			'password': pswd,
		},
		timeout: 5000,
		success: function(data, status, xhr) {
			if (data.code == 1) {
				$('#USER_login_status').html('注册成功');
				//setTimeout(function(){
				//		window.location = data.referer || './';
				//	},1000
				//);					
			} else {
				if (data.code == -1) {
					$('#USER_login_pswd').val('');
					$('#USER_login_pswd').focus();
				}
				$('#USER_login_status').html(data.message);
			}
		},
		error: function(data) {
			$('#USER_login_user').val('');
			$('#USER_login_user').focus();
			$('#USER_login_pswd').val('');
			$('#USER_login_status').html(data.responseText);

		},
		dataType: 'json'
	});
} 
