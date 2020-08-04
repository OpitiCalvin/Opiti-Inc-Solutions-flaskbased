from geoalchemy2.shape import to_shape
# from sqlalchemy import func
from geojson import Feature, FeatureCollection
import collections

class GeoJSONSerializer:
    geojson_list = []
    # __geom_field__ = 'geom'

    def __init__(self, geoData):
        self.geoObj = geoData

        self.__parseGeoData()
        
    def __parseGeoData(self):
        if isinstance(self.geoObj, list):
            for feat in self.geoObj:
                feat_shape = to_shape(feat.geom)
                # feat_properties = feat.__dict__
                # try:
                #     del(feat_properties['geom'])
                #     del(feat_properties['_sa_instance_state'])
                # except KeyError as e:
                #     raise (f"Column `geom` not found. {e}")
                # # feat_properties = feat_properties.pop('geom', None)
                feat_properties = {
                    "name": feat.name
                }

                final_geojson = Feature(
                    geometry = feat_shape,
                    properties = feat_properties
                )
                self.geojson_list.append(final_geojson)
            
        else:
            # working with single model class object record.
            feat_shape = to_shape(self.geoObj.geom)
            # feat_properties = self.geoObj.__dict__
            # try:
            #     del(feat_properties['geom'])
            #     del(feat_properties['_sa_instance_state'])
            # except KeyError as e:
            #     raise (f"Column `geom` not found. {e}")
            # # feat_properties = feat_properties.pop('geom', None)
            feat_properties = {
                "name": self.geoObj.name
            }

            final_geojson = Feature(
                geometry = feat_shape,
                properties = feat_properties
            )
            self.geojson_list.append(final_geojson)

    def toGeojson(self):
        geojson_collection = FeatureCollection(self.geojson_list)
        return geojson_collection
        # return self.geojson_list
