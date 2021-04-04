$(document).ready(function() {
	$('#like_btn').click(function(){
    	var moreImagesIdVar;
    	moreImagesIdVar = $(this).attr('data-image_id');
    
    	$.get('/RateMyWalk/like_image/',
    		{'image_id': moreImagesIdVar},
    		function(data) {
    			$('#like_count').html(data);
    			$('#like_btn').hide();
    		})
    });
});