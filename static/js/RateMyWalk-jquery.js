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
    
    /*
    $("#myDropdown").hover(
		function() {
            $('ul.list-group',this).stop(true, true).slideDown('500');
        },
        function() {
            $('ul.list-group',this).stop(true, true).slideUp('300');
    });
    */
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
	
	$('#attribute').on('change', function(){
		$('#sorting').submit();
	});
});
