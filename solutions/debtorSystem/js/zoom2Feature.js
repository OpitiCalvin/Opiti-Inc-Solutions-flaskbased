function zoomToCoordinates(coordinates, zoom) 
{
	map.getView().setCenter(coordinates);
    map.getView().setZoom(zoom);
}