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
    
    var bgOn;
    $('.p-2').hover(
    	function() {
            bgOn = $(this).css('background-color');
    		$(this).css('background-color', 'black');
    	},
    	function() {
    		$(this).css('background-color', bgOn);
    });
    
    
    $("#top-5-walks").hover(
		function() {
            $('ul.file_menu').stop(true, true).slideDown('medium');
        },
        function() {
            $('ul.file_menu').stop(true, true).slideUp('medium');
    });
        
});
