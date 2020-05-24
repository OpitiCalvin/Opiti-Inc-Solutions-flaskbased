var osmLayer = L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap<\/a> contributors'
});

var oslTilelayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
  '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
  'Imagery Â© <a href="https://www.mapbox.com/">Mapbox</a>',
  id: 'mapbox.light'
});

var streets = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 18,
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
  '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
  'Imagery Â© <a href="https://www.mapbox.com/">Mapbox</a>',
  id: 'mapbox.streets'
});

// var map = L.map(document.getElementById('map'), {zoomControl: true}).setView([-26.21,28.03], 15);
var map = L.map(document.getElementById('map'),{
  center: [-26.21,28.03],
  zoom: 15,
  layers: [osmLayer, oslTilelayer, streets]
});

var baseMaps = {
  "Mapbox Light": oslTilelayer,
  "Mapbox Streets": streets,
  "OSM": osmLayer
};

var drawnItems = new L.FeatureGroup()
map.addLayer(drawnItems)

var overlayMaps = {"Screen Digitized": drawnItems};
var lc = L.control.layers(baseMaps, overlayMaps, {collapsed: true}).addTo(map);

var drawControl = new L.Control.Draw({
  position: 'bottomright',
  draw:{
    polygon: {
      shapeOptions: {
        color: 'purple'
      },
      allowIntersection: false,
      drawError: {
        color: 'orange',
        timeout: 1000
      },
      showArea: true,
      metric: true,
      repeatMode: false,
    },
    marker: false,
    polyline: {
      shapeOptions: {
        color: 'red'
      },
      allowIntersection: false,
      drawError: {
        color: 'orange',
        timeout: 1000
      },
      repeatMode: false,
    },
    circlemarker: false,
    rectangle: {
      shapeOptions: {
        color: 'green'
      },
      showArea: true,
      metric: true,
      repeatMode: false,
    },
    circle: {
      shapeOptions: {
        color: 'steelblue'
      },
      showArea: true,
      metric: true,
      repeatMode: false,
    },
  },
  edit: {
    featureGroup: drawnItems
  }
});

map.addControl(drawControl);
map.on(L.Draw.Event.CREATED, function (e) {
  var layer = e.layer;
  var type = e.layerType;

  drawnItems.addLayer(layer);

  var jsonContainer = $('#json-container');

  // on click, convert to geoJSON
  document.getElementById("export").onclick = function (e){
    e.preventDefault();
    // get output format option selected
    outputFormat = document.getElementById('outputFormat').value;
    if (outputFormat === "ESRI Shapefile"){
      alert('Functionality not available yet. Please consider GeoJSON format for now. Thanks')
    } else if (outputFormat === "GeoJSON"){
      // create a new featureGroup
      var items2Export = new L.FeatureGroup();
      drawnItems.eachLayer(function (layer) {
        // load all non-circle features to new feature group
        if (!(layer instanceof L.Circle)) {
          items2Export.addLayer(layer);
        }
        else{
          // convert circle feature to turf.circle (basically a polygon with 64 vertices) then...
           // add to new feature group for exporting as geojson
          var theCenterPt = layer.getLatLng();
          var epiCenter = [theCenterPt.lng, theCenterPt.lat];
          var radius = layer.getRadius();

          // Turf Circle
          var options = {steps: 64, units: 'meters'};
          var turfCircle = turf.circle(epiCenter, radius, options);
          var NewTurfCircle = new L.GeoJSON(turfCircle, {color:"steelblue"});    
          
          items2Export.addLayer(NewTurfCircle);
        }
      });

      var data = items2Export.toGeoJSON();

      if (data['features'].length){
        // Stringify the GeoJSON
        var convertedData = 'text/json; charset=utf-8,' + encodeURIComponent(JSON.stringify(data, undefined, 4));
        var str = JSON.stringify(data, undefined, 4);
        // document.getElementById("geojson_data").innerHTML = str;
        // document.getElementById("json-container").innerHTML = str;

        var error = false;
        try {
          var json = JSON.parse(str);
        }
        catch (f) {
          error = true;
        }

        jsonContainer
        .jsonPresenter('destroy')
        .jsonPresenter({json: json });

        // // manual download of data
        // document.getElementById('download').onclick = function (e){
        //   document.getElementById('download').setAttribute('href', 'data:' + convertedData);
        //   document.getElementById('download').setAttribute('download','data.geojson');  
        // }
        // automated data download with export button
        let downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute('href', 'data:' + convertedData);
        downloadAnchorNode.setAttribute('download','data.geojson');
        downloadAnchorNode.click();
        downloadAnchorNode.remove()
      } else {
        jsonContainer
        .jsonPresenter('destroy')
        alert("Cannot export an empty geoJSON/layer.");
      }
    } else {
      alert("System could not understand selected output format option. Please recheck your selection.")
    }
  }
  
});