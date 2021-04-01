$(document).ready(function() {

    
    $('#unauthenticated-user-rating').click(function() {
        alert('Please Log In to rate this walk');
    });
    
    $('.btn btn-primary').hover(
    	function() {
    		$(this).css('background-color', 'grey');
    	},
    	function() {
    		$(this).css('background-color', 'black');
    	},
	});
	
	$('.navbarText').hover(
		function() {
			$(this).css('background-color', 'grey');
		},
    	function() {
			$(this).css('background-color', 'black');
		},
	});
	
	
	$('.rango-page-add').click(function() {
		var categoryid = $(this).attr('data-categoryid');
		var url = $(this).attr('data-url');
		var clickedButton = $(this);
		
		$.get('/RateMyWalk/rateWalk/',
			{'ratewalk_id': ratewalk, 'link': url},
			function(data) {
				$('#rateWalkYourself').html(data);
    			clickedButton.hide();
			})
	})
});
