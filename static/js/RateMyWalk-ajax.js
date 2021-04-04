$(document).ready(function() {

    
    $('#like_btn').click(function(){
    	var moreImagesIdVar;
    	moreImagesIdVar = $(this).attr('data-image_id');
    
    	$.get('rate_my_walk/like-image/',
    		{'data-image_id': moreImagesIdVar},
    		function(data) {
    			$('#like_count').html(data);
    			$('#like_btn').hide();
    		}
    });
});