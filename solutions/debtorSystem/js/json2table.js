function json2table(json, classes) {
    var cols = Object.keys(json[0]);
    var headerRow = '';
    var bodyRows = '';
    var classes = classes || '';
    
    cols.map(function(col){
        headerRow += '<th>' + capitaliseFirstLetter(col) + '</th>';
    });

    json.map(function(row) {
        bodyRows += '<tr>';
        // To do : Loop over object properties and create cells
	cols.map(function(colName){
	    bodyRows += '<td>' + row[colName] + '<td>';
	});
	bodyRows += '</tr>';
    });

    return 'table class="' + 
	    classes +
	    '"><thead><tr>' + 
	    headerRow +
	    '</tr></thead><body>' +
	    bodyRows +
	    '</tbody></table>';
    
}

function capitaliseFirstLetter(string){
    return string.charAt(0).toUpperCase() + string.slice(1);
}