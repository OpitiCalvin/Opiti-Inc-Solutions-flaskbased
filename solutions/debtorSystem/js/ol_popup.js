/**
* Elements that make up the popup
**/
var container  = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');

/**
* Create an overlay to anchor the popup to the map
**/
var overlay = new ol.Overlay({
	element : container,
	autoPan : true,
	autoPanAnimation : {
		duration : 250
	}
});

/**
* add a click handler to hide the popup.
* @return {boolean} Don't follow the href.
*/
closer.onclick = function(){
	overlay.setPosition(undefined);
	closer.blur();
	return false;
};

map.addOverlay(overlay);
/** 
* Add a click handler to the map to render the popup.
*/
map.on('singleclick', function(evt){
	var coordinate = evt.coordinate;
	var hdms = ol.coordinate.toStringHDMS(ol.proj.toLonLat(coordinate));
	
	content.innerHTML = '<p>You Clicked here: </p><code>' + hdms + '</code>';
	overlay.setPosition(coordinate);
});