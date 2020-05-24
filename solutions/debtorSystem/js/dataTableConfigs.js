$(document).ready(function(){
	  var prov_table = $('#table_prov').DataTable({
		"scrollX": true,
		// "autoWidth": true, 
		"scrollY": "300px",
		"paging": false,
		"searching": false,
		"ordering": false,
		
	  });
	$('#table_prov tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            prov_table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
	} );
 
    // $('#button').click( function () {
        // table.row('.selected').remove().draw( false );
    // } );
});

$(document).ready(function(){
  var ward_table = $('#table_ward').DataTable({
    "scrollX": true,
    "scrollY": "300px",
	// "autoWidth": true, 
    "paging": false,
    "searching": false,
    "ordering": false,
	// "columnDefs": [
            // { "width": '50px', "targets": 0 }
        // ],
        // "fixedColumns": true
  });
	$('#table_ward tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            ward_table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
	});
});
$(document).ready(function(){
  var bldg_table = $('#table_bldg').DataTable({
    "scrollX": true,
    "scrollY": "300px",
	// "autoWidth": true, 
    "paging": false,
    "searching": false,
    "ordering": false
  });
  
  $('#table_bldg tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            bldg_table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
			/* Call a function to zoom to the feature selected */
			var centroid = $(this).find('td').eq(4).text().split(',');
			var center = [parseFloat(centroid[0]),parseFloat(centroid[1])]
			zoomToCoordinates(center, 19)
			//console.log(center)
			//map.getView().setCenter(center);
            //map.getView().setZoom(19);
        }
	} );
});
$(document).ready(function(){
  var city_table = $('#table_city').DataTable({
    "scrollX": true,
    "scrollY": "300px",
	// "autoWidth": true, 
    "paging": false,
    "searching": false,
    "ordering": false
  });
	$('#table_city tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            city_table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
	});
});

