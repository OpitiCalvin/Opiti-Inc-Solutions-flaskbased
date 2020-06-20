
var raster = new ol.layer.Tile({
  source: new ol.source.OSM()
});

var county = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: '/accidents/countyGeoJSON',
    format: new ol.format.GeoJSON()
  })
});

var accident_source = new ol.source.Vector({
    url: '/accidents/accidentsGeoJSON/?county=null',
    format: new ol.format.GeoJSON()
  });

window.accident = new ol.layer.Vector({
  source: accident_source
});

var map = new ol.Map({
  layers: [raster, county, accident],
  // layers: ['raster'],
  target: 'map',
  view: new ol.View({
    // center: [0, 0],
    center: [-44398.4082, 7162552.5802],
    zoom: 6
  })
});

var select = new ol.interaction.Select({
  layers:[county]
});

map.addInteraction(select);

select.on('select', function(e) {
  console.log(e.target.getFeatures().getArray()[0].get('name'))
  // accident.setSource({
  //   url: '/accidents/accidentsGeoJSON/?county='+e.target.getFeatures().getArray()[0].get('name'),
  //   format: new ol.format.GeoJSON()
  // });
  accident.getSource().setUrl('/accidents/accidentsGeoJSON/?county='+e.target.getFeatures().getArray()[0].get('name'));
  accident.getSource().refresh();
  
});
