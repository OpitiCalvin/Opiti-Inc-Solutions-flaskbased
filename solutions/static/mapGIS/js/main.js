var osmLayer = L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap<\/a> contributors'
});

var oslTilelayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
	'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
	'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox.light'
});

var streets = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
	maxZoom: 18,
	attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
	'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
	'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
	id: 'mapbox.streets'
});

// Determine location of user using user's IP address.
// var pos = L.GeoIP.getPosition();
// console.log(pos);

//var mymap = L.map('mapid').setView([51.505, -0.09], 13);
var mymap = L.map('mapid',{
	center: [-26.21,28.03], //-26.206902, 28.031237
	zoom: 13,
	layers: [osmLayer,oslTilelayer,streets]
});

var baseMaps = {
	"Mapbox Light": oslTilelayer,
	"Mapbox Streets": streets,
	"OSM": osmLayer
};

var overlayMaps = {
};

// console.log(baseMaps["OSM"]._url)
var lc = L.control.layers(baseMaps, overlayMaps, { collapsed: true }).addTo(mymap);

var popup = L.popup();