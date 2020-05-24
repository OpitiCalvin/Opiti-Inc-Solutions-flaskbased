var json;

function processFiles(evt){
	var files = evt.target.files; // FileList object
	
	for (var i=0; i < files.length; i++){
		if (files[i].name.slice(-3) == 'zip') {
			// For ZIP files
			var lyrName = humanize(files[i].name.split('.')[0]);
			// Dynamic layer name variables
			var lyr = L.geoJson({features:[]},{
				onEachFeature: function popUp(f,l){
					// var out = [];
					var tab_content = "<table id='popTable' class='table table-striped table-bordered table-sm'> <tbody>";
					var tab_end = "</tbody> </table>";
					if (f.properties) {

						// for (var key in f.properties) {
						// 	out.push (key+": "+f.properties[key]);
						// }

						for (var key in f.properties) {
							// out.push (key+": "+f.properties[key]);
							tab_content = tab_content + 
								"<tr>"+
								  "<th scope='row'>" + key + "</th>"+
								  "<td>" + f.properties[key] + "</td>"+
								"</tr>"
						}

						tab_content = tab_content + tab_end;
						// l.bindPopup(out.join("<br />"));
						l.bindPopup(tab_content);
					}
				},
				style: function(feature) {
							return {
									opacity: 1,
									fillOpacity: 0.4,
									radius: 6,
									// color: feature.properties.__color__
									color: 'blue'
							}
					},
					pointToLayer: function(feature, latlng) {
							return L.circleMarker(latlng, {
									opacity: 1,
									fillOpacity: 0.4,
									// color: feature.properties.__color__
									color: 'blue'
							});
					}
				
			}).addTo(mymap);
			layerList();

			var reader = new FileReader();
			reader.onload = function(e){
				var datafile = reader.result;
				// console.log(dataURL);
				shp(datafile).then(function(data){
					lyr.addData(data);
					mymap.fitBounds(lyr.getBounds());
					lc.addOverlay(lyr,""+ lyrName + "")
				})
			};
			reader.readAsArrayBuffer(files[i]);
		}
		else if (files[i].name.slice(-7) == 'geojson') {
			// Handle geojson files
			var lyrName = humanize(files[i].name.split('.')[0]);

			// Dynamic layer name variables
			var lyr = L.geoJson({features:[]},{
				onEachFeature: function popUp(f,l){
					// var out = [];
					var tab_content = "<table id='popTable' class='table table-striped table-bordered table-sm'> <tbody>";
					var tab_end = "</tbody> </table>";
					if (f.properties) {
						// for (var key in f.properties) {
						// 	out.push (key+": "+f.properties[key]);
						// }
						for (var key in f.properties) {
							// out.push (key+": "+f.properties[key]);
							tab_content = tab_content + 
								"<tr>"+
								  "<th scope='row'>" + key + "</th>"+
								  "<td>" + f.properties[key] + "</td>"+
								"</tr>"
						}

						tab_content = tab_content + tab_end;
						// l.bindPopup(out.join("<br />"));
						l.bindPopup(tab_content);
					}
				},
				style: function(feature) {
							return {
									opacity: 1,
									fillOpacity: 0.4,
									radius: 6,
									// color: feature.properties.__color__
									color: 'blue'
							}
					},
					pointToLayer: function(feature, latlng) {
							return L.circleMarker(latlng, {
									opacity: 1,
									fillOpacity: 0.4,
									// color: feature.properties.__color__
									color: 'blue'
							});
					}
				
			}).addTo(mymap);
			layerList();

			var reader = new FileReader();

			reader.onload = function (theFile) {
				try {
					json = JSON.parse(reader.result);
					lyr.addData(json);
					mymap.fitBounds(lyr.getBounds());

					lc.addOverlay(lyr,""+ lyrName + "")
				} catch (ex) {
					alert('Error when trying to parse json = ' + ex);
				}
			};
			reader.readAsText(files[i]);
		}
		else {
			alert(" Check you input file(s) if supported.")
		}
	}
}

document.getElementById('file_input').addEventListener('change', processFiles, false);

function layerList(){
	var t_layers = [];
	mymap.eachLayer(function(layer){
		if(layer instanceof L.geoJson ){
			t_layers.push(layer)
		}
	});
	// console.log(t_layers);
}

// A function to convert string (file names to human form - remove spaces and capitalise 1st Char of each word.)
function humanize(str) {
	var frags = str.split('_');
	for (i=0; i<frags.length; i++) {
		frags[i] = frags[i].charAt(0).toUpperCase() + frags[i].slice(1);
	}
	return frags.join(' ');
}
