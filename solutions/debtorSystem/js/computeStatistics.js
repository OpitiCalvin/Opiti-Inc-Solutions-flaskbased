/**
* Computation of Summary Statistics for Buildings Layer.
***********************************************************
*/

/**
* COUNT of all building features - vred_builds.
*/
function computeCount(geojsonLayer){
	var count = 0;
	var i = 0;
	var featArray = Object.keys(geojsonLayer.features);
	
	for (var i=0; i<featArray.length;i++){
		//console.log(i+1)
		count = i+1
		//console.log(count)
		//document.getElementById('featCountStats').innerHTML = count;
	}
	// do{
		// count += i;
		// //console.log(count);
		// i++;
	// }
	// while (i < featArray.length);
	// console.log(count);
	
	return count
};

/**
* Sum of Owed Amounts on a layer - vred_builds.
*/
function computeSum(geojsonLayer){
	var sum = 0;
	var i = 0;
	var noFeat = Object.keys(geojsonLayer.features).length;
	var featArray
	
	for (i=0;i<noFeat;i++){
		sum += Object.values(geojsonLayer.features[i].properties)[3];
		//console.log(sum);
	}
	return sum
}

/**
* MEAN amount owed based on layer - vred_builds.
*/
function computeAverage(geojsonLayer){
	var n = computeCount(geojsonLayer);
	var sigma = computeSum(geojsonLayer);
	
	return sigma/n;
}

function computeMinMax(geojsonLayer){
	var amountArray=[];
	var noFeat = Object.keys(geojsonLayer.features).length;
	
	for (var i=0;i<noFeat;i++){
		amountArray.push(Object.values(geojsonLayer.features[i].properties)[3]);
		//console.log(sum);
	}
	
	var minVal = Math.min(...amountArray);
	var maxVal = Math.max(...amountArray);
	
	return [minVal,maxVal]	
}

function countOverLimit(geojsonLayer,limit){
	var baseline = limit || 500;
	var amountArray=[];
	var count = 0;
	var noFeat = Object.keys(geojsonLayer.features).length;
	
	for (var i=0;i<noFeat;i++){
		amountArray.push(Object.values(geojsonLayer.features[i].properties)[3]);
		//console.log(sum);
	}
	for (var j=0; j <amountArray.length;j++){
		if (amountArray[j] >= 500){
			count += 1
		}
	}
	return [baseline,count]
}

var featCount = computeCount(vred_builds);
document.getElementById('featCountStats').innerHTML = '<p><a href="#">COUNT</a></p>'+ featCount

var sumOwed = computeSum(vred_builds);
document.getElementById('SumAmountStats').innerHTML = '<p><a href="#">TOTAL AREAS</a></p>ZAR '+ sumOwed;

var meanOwed = computeAverage(vred_builds);
document.getElementById('meanAmountStats').innerHTML = '<p><a href="#">MEAN AREAS</a></p>ZAR '+ meanOwed;
var lims = computeMinMax(vred_builds);
document.getElementById('maxStats').innerHTML = '<p><a href="#">HIGHEST OWED AMOUNT</a></p> ZAR '+ lims[1];
document.getElementById('minStats').innerHTML = '<p><a href="#">LOWEST OWED AMOUNT</a></p> ZAR '+ lims[0];
var overLim = countOverLimit(vred_builds,750);
document.getElementById('limitStats').innerHTML = '<p><a href="#">COUNT OVER ZAR '+overLim[0]+'</a></p> '+ overLim[1];