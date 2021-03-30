$(document).ready(function() {

    
    $('#unauthenticated-user-rating').click(function() {
        alert('Please Log In to rate this walk');
    });
    
    $('.btn btn-primary').hover(
    	function() {
    		$(this).css('background-color', 'grey');
    		$(this).css('color', 'black');
    	},
    	function() {
    		$(this).css('background-color', 'white');
    	},
	});

})

