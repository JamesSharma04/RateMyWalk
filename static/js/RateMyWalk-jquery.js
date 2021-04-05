$(document).ready(function() {
    
    /* Feather icon script for walk.html */
    feather.replace()
    
    /* Informs user they must log in to rate a walk */
    $('#unauthenticated-user-rating').click(function() {
        alert('Please Log In to rate this walk');
    });
    
    // on hovering over buttons, buttons change to grey
    $('.navbarText').hover(
    	function() {
    		$(this).css('color', 'grey');
    	},
    	function() {
    		$(this).css('color', 'white');
    });
    
    // on hovering over contact us in footer, text change to grey
    $('#contact_usFooter').hover(
    	function() {
    		$(this).css('color', 'grey');
    	},
    	function() {
    		$(this).css('color', 'white');
    });
    
    // delete walk button
    $("#delete-walk").click(function() {
    	if (!confirm('Are you sure you want to delete this page?')){
    	return false;
    	}
    });
    
    // logout warning message
    $("#logout-button").click(function() {
    	if (!confirm('Are you sure you want to logout?')){
    	return false;
    	}
    });
	
    /* Allows walks to be sorted on a condition in walks.html */
	$('#attribute').on('change', function(){
		$('#sorting').submit();
	});
    
    /* For resizing form input boxes height */
    $('.resizeForm').on('keydown input', function() {
        this.style.removeProperty('height');
        this.style.height = (this.scrollHeight+2) + 'px';
    }).on('mousedown focus', function() {
        this.style.removeProperty('height');
        this.style.height = (this.scrollHeight+2) + 'px';
    });
    
});
