$(document).ready(function() {
    
    /* Feather icon script for walk.html */
    feather.replace()
    
    /* Informs user they must log in to rate a walk */
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
	
    /* Allows walks to be sorted on a condition in walks.html */
	$('#attribute').on('change', function(){
		$('#sorting').submit();
	});
    
    
    $('.resizeForm').on('keydown input', function() {
        //Auto-expanding textarea
        this.style.removeProperty('height');
        this.style.height = (this.scrollHeight+2) + 'px';
    }).on('mousedown focus', function() {
        //Do this on focus, to allow textarea to animate to height...
        this.style.removeProperty('height');
        this.style.height = (this.scrollHeight+2) + 'px';
    });
    
});
