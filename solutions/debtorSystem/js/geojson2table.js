function geojson2table(geojson, tname) {
	noFeat = Object.keys(geojson.features).length;
	var cols = Object.keys(geojson.features[0].properties);
	//var rowsss = Object.values(geojson.features[0].properties);
    var headerRow = '';
    var bodyRows = '';
    var t_name = tname;
	var i;
	var j;
	var l;
    
	for (i=0;i<cols.length;i++){
		headerRow +='<th>' + capitaliseFirstLetter(cols[i]) + '</th>';
	}	
	//add centroid coordinates to headerRow
	headerRow += '<th>Centroid</th>';
	
	var coordArray = getCoordinates(geojson);
	var centArrary = getCentroid(coordArray);
	
	for (j=0;j<noFeat;j++){
		bodyRows += '<tr>';
		var rowsss = Object.values(geojson.features[j].properties)
		rowsss[rowsss.length] = centArrary[j]
		// + ',['+centArrary[j]+']';
		var rows = check4Nulls(rowsss);
		for (l=0;l<rows.length;l++){
			bodyRows += '<td>' + rows[l] + '</td>';
		}
		bodyRows += '</tr>';
	}	
	return '<table id="'+ t_name +'" class="table table-striped table-bordered nowrap" cellspacing="1" width="100%"><thead><tr>' + 
	    headerRow +
	    '</tr></thead><body>' +
	    bodyRows +
	    '</tbody></table>';    
}

function getCoordinates(geojson){
	var coords = []
	noFeat = Object.keys(geojson.features).length;
	for (var k=0;k<noFeat;k++){
		coords.push(Object.values(geojson.features[k].geometry.coordinates[0]))
	}
	return coords
}
function getCentroid(coord) 
{
	len = coord.length;
	centroids = []
	for (var m=0;m<len;m++){
		var center = coord[m][0].reduce(function(x,y){
			return [x[0] + y[0]/coord[m][0].length, x[1] + y[1]/coord[m][0].length] 
		}, [0,0])
		if (Number.isNaN(center[0])){
			var center2 = coord[m].reduce(function(x,y){
				return [x[0] + y[0]/coord[m].length, x[1] + y[1]/coord[m].length] 
			}, [0,0])
			centroids.push(center2)	
		}
		else{
			centroids.push(center)
		}
	}
	// var center = coord.reduce(function (x,y) {
		// return [x[0] + y[0]/coord.length, x[1] + y[1]/coord.length] 
	// }, [0,0])
	// return center;
	return centroids
}

function capitaliseFirstLetter(string){
	var stringOut = string.toLowerCase()
	return stringOut.charAt(0).toUpperCase() + stringOut.slice(1);
}

function check4Nulls(array){
	var newArr = []
	for (i=0;i < array.length;i++){
		if (typeof array[i] !== 'undefined' && array[i] !== null) {
			newArr.push(array[i]);
		}
		else{
			array[i]='Null';
			newArr.push(array[i]);
		}
	};
	return newArr;
};