
var raster = new ol.layer.Tile({
  source: new ol.source.OSM()
});

var county = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: '/accidents/countyGeoJSON',
    format: new ol.format.GeoJSON()
  })
});
// heatmap section 
let heatmapLayer = new ol.layer.Heatmap({
  // source: new VectorSource(),
  source: new ol.source.Vector(),
  radius: 8,
  // shadow: 500,
  blur:15
});
// end of heatmap sectipn

var accident_source = new ol.source.Vector({
    url: '/accidents/accidentsGeoJSON/?county=null',
    format: new ol.format.GeoJSON()
  });

var accident = new ol.layer.Vector({
  // visible: false,
  source: accident_source
});

var map = new ol.Map({
  layers: [raster, county, accident, heatmapLayer],
  // layers: [raster, county, heatmapLayer],
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
  $("#spinner").prop('hidden', false);
  // console.log(e.target.getFeatures().getArray()[0].get('name'))
  // accident.setSource({
  //   url: '/accidents/accidentsGeoJSON/?county='+e.target.getFeatures().getArray()[0].get('name'),
  //   format: new ol.format.GeoJSON()
  // });
  
  let extent = e.target.getFeatures().getArray()[0].getGeometry().getExtent();
  map.getView().fit(extent);
  accident.getSource().setUrl('/accidents/accidentsGeoJSON/?county='+e.target.getFeatures().getArray()[0].get('name'));
  accident.getSource().refresh();
  fetch('/accidents/accidentsStatistics/?county='+e.target.getFeatures().getArray()[0].get('name'))
  .then(response =>{
    if (!response.ok){
      throw new Error(response.json());
    }
    return response.json();
  })
  .then(responseData => {
    $("#spinner").prop('hidden', true);
    flash("Query for accident data succcessful",{
      'bgColor': "#51B155"
    });
    // heatmap section
    // heatmapLayer.getSource().clear();
    let featList = accident.getSource().getFeatures();  //  this.source  get the target features 
    // console.log(featList[0]);
    for(let item of featList ) {              //  copy the feature to the heatmap layer
          let geometry = item.get('geometry');
          let coordinate = geometry.flatCoordinates;
          let feature = new ol.Feature({
              geometry: new ol.geom.Point(coordinate),
          })
          heatmapLayer.getSource().addFeature(feature);
    }
    // heatmapLayer.getSource().refresh();
    // this.map.addLayer(heatmapLayer);  //  add heatmap layer to map

    // end of heatmap section

    // graph function will go here
    let dataLabels = []
    let no_of_accidents = []
    let no_of_casualties = []
    let no_of_vehicles = []

    for (level in responseData){
      dataLabels.push("Level "+level);
      no_of_accidents.push(responseData[level]["accident_count"])
      no_of_casualties.push(responseData[level]['casualty_total'])
      no_of_vehicles.push(responseData[level]["vehicle_total"])
    }

    $('#myChart').empty();
    var ctx = document.getElementById('myChart').getContext('2d');
		var severityData = {
      // labels: ["Level 1", "Level 2", "Level 3"],
      labels: dataLabels,
			datasets: [
				{
					label: "No of Accidents",
					backgroundColor: "rgba(54, 162, 235, 0.2)",
					borderColor: "rgba(54, 162, 235, 1)",
					borderWidth: 1,
          // data: [29,331,1384]
          data: no_of_accidents
				},
				{
					label: "No of Casulties",
					backgroundColor: "rgba(255, 99, 132, 0.2)",
					borderColor: "rgba(255, 99, 132, 1)",
					borderWidth: 1,
          // data: [47,461,1809]
          data: no_of_casualties
				},
				{
					label: "No of Vehicles",
					backgroundColor: "rgba(255, 206, 86, 0.2)",
					borderColor: "rgba(255, 206, 86, 1)",
					borderWidth: 1,
          // data: [43,599,2616]
          data: no_of_vehicles
				}
			]
		};
		
		var myChart = new Chart(ctx, {
			type: 'bar',
			data: severityData,
			options: {
				barValueSpacing: 20,
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						}
					}]
        },
        title: {
          display: true,
          text: 'Statistics by Accident Severity: County='+e.target.getFeatures().getArray()[0].get('name')
        }
			}
		});
    
  })
  .catch(error => {
    $("#spinner").prop('hidden', true);
    flash(error,{
      'bgColor': "#E62229"
    });
    
  })

  // if (accident.getSource().getState() === 'ready'){
  //   console.log(accident.getSource().getState());
  //   $("#spinner").prop('hidden', true);
  // }
  
});
