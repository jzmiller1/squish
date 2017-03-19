from datetime import datetime
import os
import subprocess

import psycopg2
from psycopg2.extensions import AsIs, ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import extras

import nlcd
import secret


def loader(path, table_name, mode, srid):
    shp2pgsql_command = " ".join([shp2pgsql_path, mode, "-s {}".format(srid),
                                 os.path.join(BASE_DIR, path),
                                 table_name])
    cursor.execute(subprocess.check_output(shp2pgsql_command, shell=True))
    conn.commit()


def reproject(table_name, geom_type, srid, schema=None):
    if schema is not None:
        table_name = schema + '.' + table_name

    cursor.execute("""ALTER TABLE %(table_name)s
                         ALTER COLUMN geom TYPE geometry(%(geom_type)s,%(srid)s)
                              USING ST_Transform(geom,%(srid)s);""",
                   {'table_name': AsIs(table_name),
                    'geom_type': AsIs(geom_type),
                    'srid': srid})
    conn.commit()


def human_time_delta(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '{} days {} hours {} minutes {} seconds'.format(days, hours,
                                                               minutes, seconds)
    elif hours > 0:
        return '{} hours {} minutes {} seconds'.format(hours, minutes, seconds)
    elif minutes > 0:
        return '{} minutes {} seconds'.format(minutes, seconds)
    else:
        return '{} seconds'.format(seconds)

### DB Settings ###
DATA_SCHEMA = 'base_data'
DB = 'real'
USER = secret.USER
PW = secret.PW
HOST = secret.HOST

### Other Settings ###
psycopg2.extensions.register_adapter(dict, extras.Json)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
raster2pgsql_path = 'C:\\"Program Files"\\PostgreSQL\\9.5\\bin\\raster2pgsql.exe'
shp2pgsql_path = 'C:\\"Program Files"\\PostgreSQL\\9.5\\bin\\shp2pgsql.exe'


### Grab the Start Time
time_start = datetime.now()

### Create a Database ###
conn = psycopg2.connect("dbname=postgres host='{}' user={} password={}".format(HOST, USER, PW))
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

### Kill all connections to the target DB ###
cursor.execute("""SELECT pg_terminate_backend(pg_stat_activity.pid)
                  FROM pg_stat_activity
                  WHERE pg_stat_activity.datname = %(db_name)s
                  AND pid <> pg_backend_pid();""",
               {'db_name': DB})

### Drop and rebuild the target DB ###
cursor.execute("""DROP DATABASE IF EXISTS %(db_name)s;""", {'db_name': AsIs(DB)})
cursor.execute("""CREATE DATABASE %(db_name)s;""", {'db_name': AsIs(DB)})
del cursor
del conn

### Spatially Enable Database ###
conn = psycopg2.connect("dbname={} host='{}' user={} password={}".format(DB, HOST, USER, PW))
cursor = conn.cursor()

cursor.execute("""CREATE EXTENSION IF NOT EXISTS postgis;""")
cursor.execute("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")

cursor.execute("""INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext)
                  VALUES ( 96630, 'sr-org', 6630, '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs ', 'PROJCS["NAD_1983_Albers",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9108"]],AUTHORITY["EPSG","4269"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["standard_parallel_1",29.5],PARAMETER["standard_parallel_2",45.5],PARAMETER["latitude_of_center",23],PARAMETER["longitude_of_center",-96],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["meters",1]]')
                  ON CONFLICT DO NOTHING""")

cursor.execute("""INSERT INTO spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext)
                  VALUES
                  (102003,
                   'esri',
                   102003,
                   '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs ',
                   'PROJCS["USA_Contiguous_Albers_Equal_Area_Conic",GEOGCS["GCS_North_American_1983",DATUM["North_American_Datum_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["longitude_of_center",-96],PARAMETER["Standard_Parallel_1",29.5],PARAMETER["Standard_Parallel_2",45.5],PARAMETER["latitude_of_center",37.5],UNIT["Meter",1],AUTHORITY["EPSG","102003"]]'
                   );"""
               )

cursor.execute("""CREATE SCHEMA %(data_schema)s;""",
               {'data_schema': AsIs(DATA_SCHEMA)})
conn.commit()

### Load NLCD Data
nlcd_data = [('data\\nlcd\\nlcd_2001_landcover_2011_edition_2014_03_311_huc8.tif', '2001'),
             ('data\\nlcd\\nlcd_2006_landcover_2011_edition_2014_03_311_huc8.tif', '2006'),
             ('data\\nlcd\\nlcd_2011_landcover_2011_edition_2014_03_311_huc8.tif', '2011')]

for path, year in nlcd_data:
    raster2pgsql_command = " ".join([raster2pgsql_path,
                                     "-I", # create spatial GiST index
                                     "-F", # add column with file name
                                     "-t 100x100",
                                     "-s 96630",
                                     os.path.join(BASE_DIR, path),
                                     "{}.nlcd{}".format(DATA_SCHEMA, year)])
    cursor.execute(subprocess.check_output(raster2pgsql_command, shell=True))
    conn.commit()

cursor.execute("""CREATE TABLE landcover (year integer,
                                          type varchar,
                                          metadata json,
                                          rast raster,
                                          id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
                                          CONSTRAINT enforce_srid_rast CHECK (st_srid(rast) = 96630));""")
conn.commit()

for year in nlcd.nlcd_years:
    cursor.execute("""INSERT INTO landcover (year, type, metadata, rast)
                      SELECT %(year)s AS year, 'NLCD' AS type, '{}' AS metadata, rast
                      FROM %(nlcd_table)s;""",
                   {"year": year,
                    "nlcd_table": AsIs("{}.nlcd{}".format(DATA_SCHEMA, year))})
    conn.commit()

######
### Import Census
######

### Spatial ###

# ###load county 1990
loader('data\\census\\spatial\\GA_county_1990_huc8.shp',
       "{}.county_1990".format(DATA_SCHEMA),
       '-c',
       102003)

# ###load county 2000
loader('data\\census\\spatial\\GA_county_2000_huc8.shp',
       "{}.county_2000".format(DATA_SCHEMA),
       '-c',
       102003)

# ###load county 2010
loader('data\\census\\spatial\\GA_county_2010_huc8.shp',
       "{}.county_2010".format(DATA_SCHEMA),
       '-c',
       102003)

# ####load tracts 1990
loader('data\\census\\spatial\\GA_tract_1990_huc8.shp',
       "{}.tract_1990".format(DATA_SCHEMA),
       '-c',
       102003)


# ###load tracts 2000
loader('data\\census\\spatial\\GA_tract_2000_huc8.shp',
       "{}.tract_2000".format(DATA_SCHEMA),
       '-c',
       102003)

# ###load tracts 2010
loader('data\\census\\spatial\\GA_tract_2010_huc8.shp',
       "{}.tract_2010".format(DATA_SCHEMA),
       '-c',
       102003)


### Load block group 1990
loader('data\\census\\spatial\\GA_blck_grp_1990_huc8.shp',
       "{}.blckgroup_1990".format(DATA_SCHEMA),
       '-c',
       102003)

### Load block group 2000
loader('data\\census\\spatial\\GA_blck_grp_2000_huc8.shp',
       "{}.blckgroup_2000".format(DATA_SCHEMA),
       '-c',
       102003)

### Load block gp 2010
loader('data\\census\\spatial\\GA_blck_grp_2010_huc8.shp',
       "{}.blckgroup_2010".format(DATA_SCHEMA),
       '-c',
       102003)

reprojects = [
              ('county_1990', 'MultiPolygon', 96630),
              ('county_2000', 'MultiPolygon', 96630),
              ('county_2010', 'MultiPolygon', 96630),
              ('tract_1990', 'MultiPolygon', 96630),
              ('tract_2000', 'MultiPolygon', 96630),
              ('tract_2010', 'MultiPolygon', 96630),
              ('blckgroup_1990', 'MultiPolygon', 96630),
              ('blckgroup_2000', 'MultiPolygon', 96630),
              ('blckgroup_2010', 'MultiPolygon', 96630)
              ]

for line in reprojects:
    reproject(line[0], line[1], line[2], schema=DATA_SCHEMA)


###
# Load NHD/NHD+
###

data = [
        ('data\\nhd\\HUC_8.shp', '{}.huc'.format(DATA_SCHEMA), '-c', 4269),
        ('data\\nhd\\HUC_10.shp', '{}.huc'.format(DATA_SCHEMA), '-a', 4269),
        ('data\\nhd\\HUC_12.shp', '{}.huc'.format(DATA_SCHEMA), '-a', 4269),
        ('data\\nhd\\NHD_Flowlines.shp', '{}.nhd_flowlines'.format(DATA_SCHEMA), '-c', 4269),
        ('data\\nhd\\Gage.shp', '{}.gages'.format(DATA_SCHEMA), '-c', 4269),
        ('data\\nhd\\Catchments.shp', '{}.catchments'.format(DATA_SCHEMA), '-c', 4269),
        ('data\\nhd\\NHD_Waterbodies.shp', '{}.nhd_waterbodies'.format(DATA_SCHEMA), '-c', 4269),
        ('data\\nhd\\nhd_p_waterbodies.shp', '{}.nhdp_waterbodies'.format(DATA_SCHEMA), '-c', 4269),
        ('data\\nhd\\NHDP_Flowlines.shp', '{}.nhdp_flowlines'.format(DATA_SCHEMA), '-c', 4269)
        ]

for line in data:
    loader(line[0], line[1], line[2], line[3])

reprojects = [
              ('{}.huc'.format(DATA_SCHEMA), 'MultiPolygon', 96630),
              ('{}.nhd_flowlines'.format(DATA_SCHEMA), 'MultiLineString', 96630),
              ('{}.nhdp_flowlines'.format(DATA_SCHEMA), 'MultiLineStringZM', 96630),
              ('{}.catchments'.format(DATA_SCHEMA), 'MultiPolygon', 96630),
              ('{}.gages'.format(DATA_SCHEMA), 'Point', 96630),
              ('{}.nhd_waterbodies'.format(DATA_SCHEMA), 'MultiPolygon', 96630),
              ('{}.nhdp_waterbodies'.format(DATA_SCHEMA), 'MultiPolygon', 96630),
              ]

for line in reprojects:
    reproject(line[0], line[1], line[2])

conn.commit()


### Aggregate all units into the units table
cursor.execute("""CREATE TABLE units (year integer,
                                      unit_type varchar,
                                      metadata json,
                                      source varchar,
                                      source_id varchar,
                                      geom geometry(MultiPolygon,96630),
                                      id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
                                      CONSTRAINT enforce_srid_geom CHECK (st_srid(geom) = 96630));""")
conn.commit()


unit_tables = ['county_1990', 'county_2000', 'county_2010', 'tract_1990',
               'tract_2000', 'tract_2010', 'blckgroup_1990', 'blckgroup_2000',
               'blckgroup_2010'
               ]
for unit_table in unit_tables:
    cursor.execute("""INSERT INTO units (year, unit_type, metadata, source, source_id, geom)
                      SELECT %(year)s AS year,
                             %(type)s AS unit_type, '{}' AS metadata, 'Census/NHGIS' AS source, gisjoin AS source_id, geom
                      FROM %(unit_table)s;""",
                   {"year": unit_table.split('_')[-1],
                    "type": unit_table.split('_')[0],
                    "unit_table": AsIs(DATA_SCHEMA + '.' + unit_table)
                    })
    conn.commit()

unit_tables = ['huc']
for unit_table in unit_tables:
    cursor.execute("""INSERT INTO units (year, unit_type, metadata, source, source_id, geom)
                      SELECT EXTRACT(YEAR FROM loaddate) AS year,
                             %(type)s AS unit_type, '{}' AS metadata, 'NHD' AS source, huc AS source_id, geom
                      FROM %(unit_table)s;""",
                   {"type": 'huc',
                    "unit_table": AsIs(DATA_SCHEMA + '.' + unit_table)
                    })
    conn.commit()


### Tabulate NLCD by Various Polygons

# Create Tables to Hold Results

cursor.execute("""CREATE TABLE tabulations (value varchar,
                                            count integer,
                                            year integer,
                                            unit uuid REFERENCES units (id),
                                            level char(3),
                                            id uuid PRIMARY KEY DEFAULT uuid_generate_v4() );""")

conn.commit()



# Tabulate Data
cursor.execute("""SELECT DISTINCT id FROM units;""",
               )

units = cursor.fetchall()
for unit_id in units:
    for year_nlcd in nlcd.nlcd_years:
        cursor.execute("""INSERT INTO tabulations (value, count, year, level, unit) (
                              SELECT value,
                                     count,
                                     %(year)s AS year,
                                     'II' AS level,
                                     %(unit_id)s AS unit
                              FROM (
                              SELECT value, SUM(count) AS count
                              FROM
                               (SELECT(pvc).*
                                FROM
                                (SELECT
                                 ST_ValueCount(ST_Clip(rast,
                                                       1,
                                                       (SELECT geom FROM units WHERE id=%(unit_id)s),
                                                        0,
                                                        True)
                                               ) AS pvc
                                 FROM landcover WHERE year = %(year)s) AS foo
                                 ) AS uncollpasedvalues
                               GROUP BY value) AS valuecounts);""",
                       {
                        "year": year_nlcd,
                        "nlcd_table": AsIs("{}.nlcd{}".format(DATA_SCHEMA, year_nlcd)),
                        "unit_id": unit_id[0]
                        })

        conn.commit()

for unit_id in units:
    for year in nlcd.nlcd_years:
        for category in nlcd.categories:
            cursor.execute("""INSERT INTO tabulations (value, count, year, level, unit) (
                              SELECT %(category)s AS category,
                                     SUM(count) AS count,
                                     year,
                                     'I' AS level,
                                     %(unit_id)s AS unit
                              FROM tabulations
                              WHERE unit = %(unit_id)s and year = %(year)s AND value IN %(category_values)s
                              GROUP BY unit, year);""",
                           {'category': category,
                            'category_values': nlcd.categories[category],
                            'year': year,
                            "unit_id": unit_id[0]
                            }
                           )
conn.commit()


### Report Time Elpased
time_finish = datetime.now()
time_elapsed = time_finish - time_start
print("FINISHED")
print(human_time_delta(time_elapsed.total_seconds()))
