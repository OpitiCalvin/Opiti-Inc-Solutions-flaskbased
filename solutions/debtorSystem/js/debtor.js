/** 
* Set global variable
*/

var projection = 'EPSG:4326';

/**
* Styles section for the layerSwitcher*/

// a basic style for the province layer
var provinceStyle = new ol.style.Style({
	fill: new ol.style.Fill({
		color: [203, 194, 185, 1]
	}),
	stroke: new ol.style.Stroke({
		color: [177, 163, 148, 0.5],
		width: 2,
		lineCap: 'round'
	})
});


var osmLayer = new ol.layer.Tile({
	title : 'OpenStreetMap',
	type: 'base',
	visible: false,
	source: new ol.source.OSM()
	});

var jhbCity = new ol.layer.Vector({
	title : 'City of Johannesburg',
	source : new ol.source.Vector({
		projection : 'EPSG:4326',
		features : (new ol.format.GeoJSON()).readFeatures(JhbCity)
		//url : '../data/CityJHB.geojson',
		//format : new ol.format.GeoJSON()
	}),
	visible: false,
});

var gProv = new ol.layer.Vector({
	title : 'Gauteng Province',
	source : new ol.source.Vector({
		projection : 'EPSG:4326',
		features : (new ol.format.GeoJSON()).readFeatures(gauteng),
		attributions:
' | &copy; <a href="https://www.opiticonsulting.com" target=_blank">Opiti Consulting</a>'
		//url : '../data/CityJHB.geojson',
		//format : new ol.format.GeoJSON()
	}),
	visible: false,
	style : provinceStyle
});

var jhbWards = new ol.layer.Vector({
	title : 'City of Jhb Wards',
	source : new ol.source.Vector({
		projection : projection,
		features : (new ol.format.GeoJSON()).readFeatures(jhb_wards)
		//url : '../data/CityJHB.geojson',
		//format : new ol.format.GeoJSON()
	}),
	visible: false,
});

var jhbBuilds = new ol.layer.Vector({
	title : 'Buildings',
	source : new ol.source.Vector({
		projection : projection,
		features : (new ol.format.GeoJSON()).readFeatures(vred_builds),
		//url : '../data/CityJHB.geojson',
		//format : new ol.format.GeoJSON()
	}),
	style : function(feature, resolution){
		var bad =  new ol.style.Style({
					fill: new ol.style.Fill({
						color: '#FF0000'
					}),
					stroke: new ol.style.Stroke({
						color: '#FF0000'
					})
				});

		var bad_avg =  new ol.style.Style({
					fill: new ol.style.Fill({
						color: '#FFAF00'
					}),
					stroke: new ol.style.Stroke({
						color: '#FFAF00'
					})
				});
		var avg =  new ol.style.Style({
					fill: new ol.style.Fill({
						color: '#D4FF00'
					}),
					stroke: new ol.style.Stroke({
						color: '#D4FF00'
					})
				});
		var avg_good =  new ol.style.Style({
					fill: new ol.style.Fill({
						color: '#7CFF00'
					}),
					stroke: new ol.style.Stroke({
						color: '#7CFF00'
					})
				});
		var good =  new ol.style.Style({
					fill: new ol.style.Fill({
						color: '#00FF00'
					}),
					stroke: new ol.style.Stroke({
						color: '#00FF00'
					})
				});
			
		if ( feature.get('billing_balance') >= 800) {
			return [bad];
		} else if(feature.get('billing_balance') >= 600) {
			return [bad_avg];
		}
		else if(feature.get('billing_balance') >= 450) {
			return [avg];
		}
		else if(feature.get('billing_balance') >= 200) {
			return [avg_good];
		}
		else{
			return [good];
		}
	}
});



var map = new ol.Map({
	//controls: ol.control.defaults({ attribution: false }).extend([
	controls: ol.control.defaults().extend([
		new ol.control.OverviewMap({ 
			view: new ol.View({
				projection: projection
			})
		}),
		new ol.control.MousePosition({coordinateFormat: ol.coordinate.createStringXY(4),
		   projection: 'EPSG: 4326',
		   //To have the mouse position coordinates place within the map
		   className: 'custom-mouse-position',
		   target: document.getElementById('mouse-position'),
		   //undefinedHTML: '&nbsp;'
		}),
	]),
	target: 'map',
	//layers: [osmLayer, gProv, jhbCity, jhbWards],
	layers: [
			new ol.layer.Group({
			'title': 'Base Maps',
			layers:[
				new ol.layer.Group({
					title: 'Water color with labels',
					type: 'base',
					combine: true,
					visible: false,
					layers: [
						new ol.layer.Tile({
							source: new ol.source.Stamen({
								layer: 'watercolor'
							})
						}),
						new ol.layer.Tile({
							source: new ol.source.Stamen({
								layer: 'terrain-labels'
							})
						})
					]
				}),
				new ol.layer.Tile({
					title: 'Water color',
					type: 'base',
					visible: false,
					source: new ol.source.Stamen({
						layer: 'watercolor'
					})
				}),
				new ol.layer.Tile({
					title: 'BingMaps Roads',
					preload : Infinity,
					type: 'base',
					visible: false,
					source: new ol.source.BingMaps({
						key : "AkUutlbjK0RiDYuyZ7ZRvGhD9n7dEcm1IWFyvSm95rwQE8Z-tWx3vcKA5JQnmkJv",
						imagerySet : 'Road',
						//culture : en-US'
					})
				}),
				new ol.layer.Tile({
					title: 'BingMaps Aerial',
					type: 'base',
					visible: false,
					preload : Infinity,
					source: new ol.source.BingMaps({
						key : "AkUutlbjK0RiDYuyZ7ZRvGhD9n7dEcm1IWFyvSm95rwQE8Z-tWx3vcKA5JQnmkJv",
						imagerySet : 'Aerial',
						//layer: 'watercolor'
					})
				}),
				new ol.layer.Tile({
					title: 'ESRI World TopoMap',
					type: 'base',
					visible: true,
					source: new ol.source.XYZ({
						attributions: 'Tiles © <a href="https://services.arcgisonline.com/ArcGIS/' +
							'rest/services/World_Topo_Map/MapServer">ArcGIS</a>',
						url: 'https://server.arcgisonline.com/ArcGIS/rest/services/' +
							'World_Topo_Map/MapServer/tile/{z}/{y}/{x}'
					})
				}),
				osmLayer
				// new ol.layer.Tile({
					// title: 'OpenStreetMap',
					// type: 'base',
					// visible: true,
					// source: new ol.source.OSM()
				// })
			]
			}),
			new ol.layer.Group({
				title: 'Overlays',
				layers: [
					gProv, jhbCity, jhbWards,jhbBuilds
					// new ol.layer.Tile({
						// title: 'Water Mosaic - June 2018',
						// source: new ol.source.XYZ({
							// url: './{z}/{x}/{-y}.png'
						// })
					// })
				]
			})
			
		],
	view : new ol.View({		
	projection: 'EPSG:4326',
	center: [28.0186,-26.1937], // Coordinates of Johannesburg
	//center: ol.proj.transform([28.03,-26.21], 'EPSG:4326', 'EPSG:3857'),
	zoom: 17
	})
	
});

// var select = new ol.interaction.Select({
// layers: [jhbWards]
// });
// map.addInteraction(select);

var layerSwitcher = new ol.control.LayerSwitcher({
	tipLabel: 'Legend', //Optional label for button
	//collapsed: false, //not working
});

map.addControl(layerSwitcher);

/**
* Loading Attribute Table for the LayerSwitcher
*/
var gpdata = geojson2table(gauteng,'table_prov');
document.getElementById('provinceTable').innerHTML = gpdata;

var warddata = geojson2table(jhb_wards,'table_ward');
document.getElementById('wardsTable').innerHTML = warddata;

var bldgdata = geojson2table(vred_builds,'table_bldg');
document.getElementById('buildingTable').innerHTML = bldgdata;

var citydata = geojson2table(JhbCity,'table_city');
document.getElementById('jhbCityTable').innerHTML = citydata;
	


