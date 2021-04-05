$(document).ready(function() {
	$('#like_btn').click(function(){
    	var walkIdVar;
    	walkIdVar = $(this).attr('data-walk_id');
    
    	$.get('/RateMyWalk/like_walk/',
    		{'walk_id': walkIdVar},
    		function(data) {
    			$('#like_count').html(data);
    			$('#like_btn').hide();
    		})
    });
});