$(document).ready(function() {
	// External links
	var current_host_link = document.createElement('a');
	current_host_link.href = window.location.href;
	var current_host = current_host_link.hostname;
	$('a').each( function() {
		var link = document.createElement('a');
		link.href = $(this).attr('href');
		var link_hostname = link.hostname;
		if (link_hostname != current_host)
			$(this).attr('target', '_blank');
	});
	// Tooltips
	$('[data-toggle="tooltip"]').tooltip();
	// Night mode
	var mode = Cookies.get('night_mode');
	if (mode != undefined)
		if (mode == "true") {
			$('#night_mode_toggle').parent().click();
			toggleNightMode();
		}
	$('#night_mode_toggle').parent().click( function() {
		toggleNightMode();
	});
});

function toggleNightMode() {
	var body = $('body');
	if ($(body).hasClass('night_mode')) {
		$(body).removeClass('night_mode');
		Cookies.set('night_mode', 'false');
	}
	else {
		$(body).addClass('night_mode');
		Cookies.set('night_mode', 'true');
	}
}