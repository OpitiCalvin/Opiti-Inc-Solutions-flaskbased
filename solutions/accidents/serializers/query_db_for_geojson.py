from flask import current_app
from sqlalchemy import create_engine

def retrieve_geojson_data(fields, geom):
    r"""
    """

    sql_text = """
        SELECT jsonb_build_object(
            'type', 'FeatureCollection',
            'features', jsonb_agg(features.feature)
        )
        FROM (
            SELECT jsonb_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON({geom})::jsonb,
                'properties', to_jsonb(inputs) - 'geom'
                ) as feature
            FROM (
                SELECT ST_Transform({geom}, {OUTPUT_SRID}) as geom {fields}
                FROM {table_name}
            ) as inputs
        ) features
    """

    table_name = 'county'
    # fields = ", name"
    fields = ','+','.join(map(str,fields))
    # geom = 'geom'
    OUTPUT_SRID = '4326'

    sql = sql_text.format(**locals())
    try:
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        conn = engine.connect()

        query = conn.execute(sql)
        data = query.cursor.fetchone()[0]

        return data

    except Exception as err:
        raise err

def retrieve_accidents_data_as_geojson(fields, county_name, county_geom, accident_geom):
    r"""
    """

    sql_text = """
        SELECT jsonb_build_object(
            'type', 'FeatureCollection',
            'features', jsonb_agg(features.feature)
        )
        FROM (
            SELECT jsonb_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON({accident_geom})::jsonb,
                'properties', to_jsonb(inputs) - 'geom'
                ) as feature
            FROM (
                SELECT ST_Transform(a.{accident_geom}, {OUTPUT_SRID}) as geom {fields}
                FROM county as c, accident as a
                WHERE c.name = '{county_name}' and ST_Within(a.{accident_geom}, c.{county_geom})
            ) as inputs
        ) features
    """
    #     SELECT a.accident_index, a.accident_severity, a.geom
    # FROM county c, accident a
    # WHERE c.name = 'Cumbria County' and
    # 	ST_Within(a.geom,c.geom)

    # table_name = 'accident'
    # fields = ", name"
    fields = ','+','.join(map(str,fields))
    # geom = 'geom'
    OUTPUT_SRID = '4326'

    sql = sql_text.format(**locals())
    try:
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        conn = engine.connect()

        query = conn.execute(sql)
        data = query.cursor.fetchone()[0]

        return data

    except Exception as err:
        raise err

def severity_stats(data):
    r"""Extracts accident data for plotting based on accident severity."""

    features = data['features']
    # print(f"Features Count: {len(features)}")

    severity_levels = []
    severity_counts={}
    for feature in features:
        severity_levels.append(feature['properties']["accident_severity"])
        if feature['properties']["accident_severity"] in severity_counts.keys():
            if 'accident_count' in severity_counts[feature['properties']["accident_severity"]].keys():
                count = severity_counts[feature['properties']["accident_severity"]]['accident_count']
                severity_counts[feature['properties']["accident_severity"]]['accident_count'] = int(count) + 1
            else:
                severity_counts[feature['properties']["accident_severity"]]['accident_count'] = 1

            if 'casualty_total' in severity_counts[feature['properties']["accident_severity"]].keys():
                casualties = severity_counts[feature['properties']["accident_severity"]]['casualty_total']
                severity_counts[feature['properties']["accident_severity"]]['casualty_total'] = int(casualties) + int(feature['properties']["number_of_casualties"])
            else:
                severity_counts[feature['properties']["accident_severity"]]['casualty_total'] = int(feature['properties']["number_of_casualties"])

            if 'vehicle_total' in severity_counts[feature['properties']["accident_severity"]].keys():
                vehicles = severity_counts[feature['properties']["accident_severity"]]['vehicle_total']
                severity_counts[feature['properties']["accident_severity"]]['vehicle_total'] = int(vehicles) + int(feature['properties']["number_of_vehicles"])
            else:
                severity_counts[feature['properties']["accident_severity"]]['vehicle_total'] = int(feature['properties']["number_of_vehicles"])
        else:
            severity_counts[feature['properties']["accident_severity"]] = {"accident_count": 1,	"casualty_total": int(feature['properties']["number_of_casualties"]) ,"vehicle_total": int(feature['properties']["number_of_vehicles"])
            }

    # print(f"Severity levels length = {len(severity_levels)}")
    # print(severity_counts)
    return severity_counts