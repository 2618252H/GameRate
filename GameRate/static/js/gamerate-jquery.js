$(document).ready(function() {
	$('navbar-toggle').hover(
		function() {
		$(this).css('color', 'red');
		},
		function() {
		$(this).css('color', 'black');
	});
	$('#search-input').keyup(function() {
		var query;
		query = $(this).val();
		$.get('/gamerateapp/suggest/',
		{'suggestion': query},
			function(data) {
				$('#categories-listing').html(data);
		})
	});

});
