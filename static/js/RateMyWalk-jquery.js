$(document).ready(function() {

    
    $('#unauthenticated-user-rating').click(function() {
        alert('Please Log In to rate this walk');
    });

    $('.navbarText').hover(
    	function() {
    		$(this).css('color', 'grey');
    	},
    	function() {
    		$(this).css('color', 'white');
    });
    
    $('#contact_usFooter').hover(
    	function() {
    		$(this).css('color', 'grey');
    	},
    	function() {
    		$(this).css('color', 'white');
    });
    
    $("#top-5-walks").hover(
		function() {
            $('ul.file_menu').stop(true, true).slideDown('medium');
        },
        function() {
            $('ul.file_menu').stop(true, true).slideUp('medium');
    });
    
    $("#delete-walk").click(function() {
    	if (!confirm('Are you sure you want to delete this page?')){
    	return false;
    	}
    });
    
    $("#logout-button").click(function() {
    	if (!confirm('Are you sure you want to logout?')){
    	return false;
    	}
    });
    
    jQuery(function($){

	function getWeather(){
		$.ajax('http://api.wunderground.com/api/c6dc8e785d943109/conditions/q/AZ/Chandler.json', {
		dataType: 'jsonp',
		success: function(json) {
			$('div#city strong').text(json.current_observation.display_location.full)
			$('div#icon').html('<img src=' + json.current_observation.icon_url + '>')
			$('div#weather').text(json.current_observation.temperature_string + " " + json.current_observation.weather);
			$('div#time').text(json.current_observation.observation_time_rfc822);
		}
	});
    }

    $('a.get_weather').click(function(e) {
    	e.preventDefault();
		$(this).hide();
		getWeather();
		$('#result').fadeIn(1000);
    });

	$('a.hide').click(function(e) {
		e.preventDefault();
		$('#result').hide();
		$('a.get_weather').show();
	})

  })
});
