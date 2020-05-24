// #FF0000	Bad
// #FFFF00	Bad-Average
// #FFFF00	Average
// #7FFF00	Average-Good
// #00FF00
function getColor(feat) {
	d = feat.get('billing_balance');
	return d > 800 ? '#c40f05' :
		   d > 600  ? '#BD0026' :
		   d > 400  ? '#E31A1C' :
		   d > 250  ? '#FC4E2A' :
		   d > 100   ? '#FD8D3C' :
					  '#FFEDA0';
};
function JSONColor(feature, resolution){
	var bad =  new ol.style.Style({
				fill: new ol.style.Fill({
					color: '#c40f05'
				}),
				stroke: new ol.style.Stroke({
					color: '#c40f05'
				})
			});

	var bad_avg =  new ol.style.Style({
				fill: new ol.style.Fill({
					color: '#BD0026'
				}),
				stroke: new ol.style.Stroke({
					color: '#BD0026'
				})
			});
	var avg =  new ol.style.Style({
				fill: new ol.style.Fill({
					color: '#E31A1C'
				}),
				stroke: new ol.style.Stroke({
					color: '#E31A1C'
				})
			});
	var avg_good =  new ol.style.Style({
				fill: new ol.style.Fill({
					color: '#FC4E2A'
				}),
				stroke: new ol.style.Stroke({
					color: '#FC4E2A'
				})
			});
	var good =  new ol.style.Style({
				fill: new ol.style.Fill({
					color: '#FD8D3C'
				}),
				stroke: new ol.style.Stroke({
					color: '#FD8D3C'
				})
			});
			
	if ( feature.get('billing_balance') >= 800) {
		return [bad];
	} else if(feature.get('billing_balance') >= 600) {
		return [bad_avg];
	}
	else if(feature.get('billing_balance') >= 400) {
		return [avg];
	}
	else if(feature.get('billing_balance') >= 250) {
		return [avg_good];
	}
	else{
		return [good];
	}
}