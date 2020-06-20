from the_app import db
from flask import current_app, render_template, request, url_for, jsonify, make_response

from accidents.views import county

from accidents.models.county import CountyModel
from accidents.models.accidents import AccidentModel

from accidents.serializers.geojson_serializer import GeoJSONSerializer
from accidents.serializers.query_db_for_geojson import retrieve_geojson_data, retrieve_accidents_data_as_geojson

@county.route('', methods=['GET'])
def accidentsIndex():
    r"""Renders the site template."""

    # geojson_data = retrieve_geojson_data(table_name='county', fields=['name','area_code','type_code','description0'], geom='geom')
    # print(geojson_data)
    # return render_template('accidents.html', geojson_data = geojson_data)
    return render_template('accidents.html')

# @county.route('/countyGeoJSON', methods=['GET'])
# def viewCountyGeoJSON():
#     r"""
#     Queries counties records and returns geometry and attribute data as geojson.

#     """

#     counties = CountyModel.query.all()
#     geoJ = GeoJSONSerializer(counties)
#     geojson_data = geoJ.toGeojson()

#     # print(geojson_data)

#     return jsonify(geojson_data)

@county.route('/countyGeoJSON', methods=['GET'])
def viewCountyGeoJSON():
    r"""
    Queries counties records and returns geometry and attribute data as geojson.

    """

    geojson_data = retrieve_geojson_data(fields=['name','area_code','type_code','description0'], geom='geom')
    # print(geojson_data)

    return jsonify(geojson_data)

@county.route('/accidentsGeoJSON/', methods=['GET'])
def viewAccidentsGeoJSON():
    r"""
    Queries accident records and returns geometry and attribute data as geojson.

    """
    args = request.args
    if 'county' in args.keys():
        print(args['county'])
        # county = args['county']
        # print(county)
        if args['county'] != 'null':
            county_select = CountyModel.query.filter_by(name=str(args['county'])).first()
            # print(county_select)
            if county_select:
                # print("county record exists")
                geojson_data = retrieve_accidents_data_as_geojson(fields=['accident_index','accident_severity'],county_name=str(args['county']), county_geom='geom',accident_geom='geom')
                # print(geojson_data)
                return jsonify(geojson_data)
            else:
               return make_response(jsonify(f"NO data available for county name {args['county']}.")),404

        else:
            return make_response(jsonify("county name not provided")),400