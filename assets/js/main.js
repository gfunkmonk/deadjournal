$(document).ready(function() {
	var current_host = window.location.href.match(/^http.?:\/\/[^/]+/);
	$('a').each( function() {
		if ($(this).attr('hostname') != current_host)
			$(this).attr('target', '_blank');
	});
});