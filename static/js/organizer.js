$(document).ready(OrganizerInit);

function OrganizerInit() {
	
	$('[data-toggle="tooltip"]').tooltip();

	// Wyłącz chwytanie obrazów (logo, nawigacja):
	$imagesOnSite = $('img');
	$imagesOnSite.on('dragstart', OnImageDrag);
	$imagesOnSite.css({'user-select':'none'});

	// Animacje nawigacji:
    $('#navigation-link-1').mouseover(function() {
        $('#navigation-image-hover-1').stop().animate({opacity:1}, 200);
    }).mouseout(function() {
        $('#navigation-image-hover-1').stop().animate({opacity:0}, 200);
    });
    
    $('#navigation-link-2').mouseover(function() {
        $('#navigation-image-hover-2').stop().animate({opacity:1}, 200);
    }).mouseout(function() {
        $('#navigation-image-hover-2').stop().animate({opacity:0}, 200);
    });
}

function OnImageDrag(event) {
	event.preventDefault();
}