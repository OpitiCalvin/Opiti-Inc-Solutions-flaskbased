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

/**
* Load billing data
*/


map.on('singleclick', function(evt){
	var buildfeat = map.forEachFeatureAtPixel(evt.pixel,
		function(buildfeat,layer) {
			if (layer == jhbBuilds){
				return buildfeat;
			}
		});
	// var wardfeat = map.forEachFeatureAtPixel(evt.pixel,
		// function(wardfeat,layer) {
			// if (layer == jhbWards){
				// return wardfeat;
			// }
		// });
	if (buildfeat) {
		var coordinate = evt.coordinate;
		
		function formatDate(date){
			var parts = date.split(',');
			month = parts[1]
			day = parts[2],
			year = parts[0];
			if (month.length < 2) month = '0' + month;
			if (day.length < 2) day = '0' + day;
			return [day, month, year].join('-');
		}
		
		content.innerHTML = '<table>' +
				'<tr><th><h3>Building ID</h3></th><th><h3> : '+ buildfeat.get('Id') +'</h3></th></tr>'+
				'<tr><td><strong>Last Payment Date</strong></td><td> : '+ formatDate(buildfeat.get('billing_last_pay')) +'</td></tr>'+
				'<tr><td><strong>Last Payment Amount</strong></td><td> : ZAR '+ buildfeat.get('billing_last_amount') +'</td></tr>'+
				'<tr><td><strong>Balance</strong></td><td> : ZAR '+ buildfeat.get('billing_balance') +'</td></tr>'+
			'</table>';
			
		overlay.setPosition(coordinate);
	}
	// if (wardfeat) {
		// //console.log(layer)
		// var coordinate = evt.coordinate;
		
		// content.innerHTML = '<table>' +
				// '<tr><th colspan="2"><h3>'+ wardfeat.get('MUNICNAME') +'</h3></th></tr>'+
				// '<tr><td><strong>Ward No.</strong></td><td> : '+ wardfeat.get('WARDNO') +'</td></tr>'+
				// '<tr><td><strong>Ward ID.</strong></td><td> : '+ wardfeat.get('WARD_ID') +'</td></tr>'+
				// '<tr><td><strong>Ward Population</strong></td><td> : '+ wardfeat.get('WARD_POP') +'</td></tr>'+
				// '<tr><td><strong>Area of Ward</strong></td><td> : '+ wardfeat.get('Area') +'</td></tr>'+
			// '</table>';
		
		// overlay.setPosition(coordinate);
	// }
});

/**
*  Generic popup function that returns data about a feature in any layer
*/
// map.on('click', function(e) {
  // let markup = '';
  // map.forEachFeatureAtPixel(e.pixel, function(feature) {
    // markup += `${markup && '<hr>'}<table>`;
    // const properties = feature.getProperties();
    // for (const property in properties) {
      // markup += `<tr><th>${property}</th><td>${properties[property]}</td></tr>`;
    // }
    // markup += '</table>';
  // }, {hitTolerance: 1});
  // if (markup) {
    // document.getElementById('popup-content').innerHTML = markup;
    // overlay.setPosition(e.coordinate);
  // } else {
    // overlay.setPosition();
  // }
// });