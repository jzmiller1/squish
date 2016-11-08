import os
import subprocess

import psycopg2
from psycopg2.extensions import AsIs, ISOLATION_LEVEL_AUTOCOMMIT

import nlcd
import secret

def loader(path, table_name, mode, srid):
    shp2pgsql_command = " ".join([shp2pgsql_path, mode, "-s {}".format(srid),
                                 os.path.join(BASE_DIR, path),
                                 table_name])
    cursor.execute(subprocess.check_output(shp2pgsql_command, shell=True))
    conn.commit()

def reproject(table_name, geom_type, srid):
    cursor.execute("""ALTER TABLE %(table_name)s
                         ALTER COLUMN geom TYPE geometry(%(geom_type)s,%(srid)s)
                              USING ST_Transform(geom,%(srid)s);""",
                   {'table_name': AsIs(table_name),
                    'geom_type': AsIs(geom_type),
                    'srid': srid})
    conn.commit()

### DB Settings ###
DB = 'data3'
USER = secret.USER
PW = secret.PW
HOST = secret.HOST


### Other Settings ###
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
raster2pgsql_path = 'C:\\"Program Files"\\PostgreSQL\\9.5\\bin\\raster2pgsql.exe'
shp2pgsql_path = 'C:\\"Program Files"\\PostgreSQL\\9.5\\bin\\shp2pgsql.exe'

### Create a Database ###
conn = psycopg2.connect("dbname=postgres host='{}' user={} password={}".format(HOST, USER, PW))
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

cursor.execute("""DROP DATABASE IF EXISTS %(db_name)s;""", {'db_name': AsIs(DB)})
cursor.execute("""CREATE DATABASE %(db_name)s;""", {'db_name': AsIs(DB)})
del cursor
del conn

### Spatially Enable Database ###
conn = psycopg2.connect("dbname={} host='{}' user={} password={}".format(DB, HOST, USER, PW))
cursor = conn.cursor()

cursor.execute("""CREATE EXTENSION IF NOT EXISTS postgis;""")

cursor.execute("""INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext)
                  VALUES ( 96630, 'sr-org', 6630, '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs ', 'PROJCS["NAD_1983_Albers",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9108"]],AUTHORITY["EPSG","4269"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["standard_parallel_1",29.5],PARAMETER["standard_parallel_2",45.5],PARAMETER["latitude_of_center",23],PARAMETER["longitude_of_center",-96],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["meters",1]]')
                  ON CONFLICT DO NOTHING""")

cursor.execute("""INSERT INTO spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext)
VALUES
( 102003,
'esri',
102003,
'+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs ',
'PROJCS["USA_Contiguous_Albers_Equal_Area_Conic",GEOGCS["GCS_North_American_1983",DATUM["North_American_Datum_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["longitude_of_center",-96],PARAMETER["Standard_Parallel_1",29.5],PARAMETER["Standard_Parallel_2",45.5],PARAMETER["latitude_of_center",37.5],UNIT["Meter",1],AUTHORITY["EPSG","102003"]]');""")

conn.commit()

### Load NLCD Data
nlcd_data = [('data\\nlcd\\nlcd_2001_landcover_2011_edition_2014_03_311_huc8.tif', '2001'),
             ('data\\nlcd\\nlcd_2006_landcover_2011_edition_2014_03_311_huc8.tif', '2006'),
             ('data\\nlcd\\nlcd_2011_landcover_2011_edition_2014_03_311_huc8.tif', '2011')]

for path, year in nlcd_data:
    raster2pgsql_command = " ".join([raster2pgsql_path,
                                     "-c",
                                     "-s 96630",
                                     os.path.join(BASE_DIR, path),
                                     "nlcd{}".format(year)])
    cursor.execute(subprocess.check_output(raster2pgsql_command, shell=True))
    conn.commit()

######
### Import Census
######

### Tabular ###
cursor.execute("""CREATE TABLE codebook (code varchar(40), description varchar(280));""")

f = open('data\\census\\tabular\\codebook.csv', 'r')
cursor.copy_from(f, 'codebook', sep=',')
f.close()

### Load Population 1990 
cursor.execute("""CREATE TABLE county_1990_pop
                 (gisjoin varchar(40), year integer, county varchar(40), countya varchar(40), divisiona varchar(40),
                  msa_cmsaa varchar(40), pmsaa varchar(40), regiona varchar(40), state varchar(40), statea varchar(40),
                  anpsadpi varchar(60), et1001 integer)""")

copy_sql = """
           COPY county_1990_pop FROM stdin WITH CSV HEADER
           DELIMITER as ','
           """
with open('data\\census\\tabular\\population\\1990\\GA_County_1990_Population.csv', 'r') as f:
    cursor.copy_expert(sql=copy_sql, file=f)
    conn.commit()


cursor.execute("""CREATE TABLE tract_1990_pop
                 (gisjoin varchar(40), year integer, tracta integer, county varchar(40), countya varchar(40), divisiona varchar(40),
                  msa_cmsaa varchar(40), pmsaa varchar(40), regiona varchar(40), state varchar(40), statea varchar(40),
                  anpsadpi varchar(60), et1001 integer)""")

copy_sql = """
           COPY tract_1990_pop FROM stdin WITH CSV HEADER
           DELIMITER as ','
           """
with open('data\\census\\tabular\\population\\1990\\GA_Tract_1990_Population.csv', 'r') as f:
    cursor.copy_expert(sql=copy_sql, file=f)
    conn.commit()

### Spatial ###
    

### Load block group 1990
loader('data\\census\\spatial\\GA_blck_grp_1990_huc8.shp',
       "blckgroup_1990",
       '-c',
       102003)

### Load block group 2000
loader('data\\census\\spatial\\GA_blck_grp_2000_huc8.shp',
       "blckgroup_2000",
       '-c',
       102003)

### Load block gp 2010
loader('data\\census\\spatial\\GA_blck_grp_2010_huc8.shp',
       "blckgroup_2010",
       '-c',
       102003)

# ####load tracts 1990
loader('data\\census\\spatial\\GA_tract_1990_huc8.shp',
       "tract_1990",
       '-c',
       102003)


# ###load tracts 2000
loader('data\\census\\spatial\\GA_tract_2000_huc8.shp',
       "tract_2000",
       '-c',
       102003)

# ###load tracts 2010
loader('data\\census\\spatial\\GA_tract_2010_huc8.shp',
       "tract_2010",
       '-c',
       102003)

# ###load county 1990
loader('data\\census\\spatial\\GA_county_1990_huc8.shp',
       "county_1990",
       '-c',
       102003)

# ###load county 2000
loader('data\\census\\spatial\\GA_county_2000_huc8.shp',
       "county_2000",
       '-c',
       102003)

# ###load county 2010
loader('data\\census\\spatial\\GA_county_2010_huc8.shp',
       "county_2010",
       '-c',
       102003)

# ###load block 1990
loader('data\\census\\spatial\\GA_blck_1990_huc8.shp',
       "block_1990",
       '-c',
       102003)

# ####load block 2000
loader('data\\census\\spatial\\GA_blck_2000_huc8.shp',
       "block_2000",
       '-c',
       102003)

# ###load block 2010
loader('data\\census\\spatial\\GA_blck_2010_huc8.shp',
       "block_2010",
       '-c',
       102003)
       


reprojects = [('blckgroup_1990', 'MultiPolygon', 96630),
              ('blckgroup_2000', 'MultiPolygon', 96630),
              ('blckgroup_2010', 'MultiPolygon', 96630),
              ('tract_1990', 'MultiPolygon', 96630),
              ('tract_2000', 'MultiPolygon', 96630),
              ('tract_2010', 'MultiPolygon', 96630),
              ('county_1990', 'MultiPolygon', 96630),
              ('county_2000', 'MultiPolygon', 96630),
              ('county_2010', 'MultiPolygon', 96630),
              ('block_1990', 'MultiPolygon', 96630),
              ('block_2000', 'MultiPolygon', 96630),
              ('block_2010', 'MultiPolygon', 96630)]

for line in reprojects:
    reproject(line[0], line[1], line[2])






data = [('data\\nhd\\HUC_8.shp', 'huc', '-c', 4926),
        ('data\\nhd\\HUC_10.shp', 'huc', '-a', 4926),
        ('data\\nhd\\NHD_Flowlines.shp', 'nhd_flowlines', '-c', 4926),
        ('data\\nhd\\Gage.shp', 'gages', '-c', 4926),
        ('data\\nhd\\Catchments.shp', 'catchments', '-c', 4926),
        ('data\\nhd\\HUC_12.shp', 'huc', '-a', 4926),
        ('data\\nhd\\NHD_Waterbodies.shp', 'nhd_waterbodies', '-c', 4926),
        ('data\\nhd\\nhd_p_waterbodies.shp', 'nhdp_waterbodies', '-c', 4926),
        ('data\\nhd\\NHDP_Flowlines.shp', 'nhdp_flowlines', '-c', 4926)]

for line in data:
    loader(line[0], line[1], line[2], line[3])

reprojects = [('huc', 'MultiPolygon', 96630),
              ('nhd_flowlines', 'MultiLineString', 96630),
              ('nhdp_flowlines', 'MultiLineStringZM', 96630),
              ('catchments', 'MultiPolygon', 96630),
              ('gages', 'Point', 96630),
              ('nhd_waterbodies', 'MultiPolygon', 96630),
              ('nhdp_waterbodies', 'MultiPolygon', 96630),]

for line in reprojects:
    reproject(line[0], line[1], line[2])

conn.commit()
            
        


