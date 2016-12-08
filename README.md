# squish
GISC 4011K class project

##Upper Chattahoochee Watershed

## Abstract:
The goal of this project is to transfer Census, National Land Cover Database (NLCD), National Hydrographic Dataset (NHD) and Transport data pertaining to the Upper Chattahoochee Watershed and  to arrange them into a systematic form. Sources for the data were extracted from the National Historical Geographic Information System(NHGIS) database, NLCD hosted by the Multi-Resolution Land Characteristics (MRLC) database, NHD, and the TIGER database from the Census website. The methods include acquiring the data, clipping the raster data, using the Windows command line to covert the files from raster to SQL, in which presented problems for the transportation data. The SQL files are loaded into the database, using a python database loader which will push the data into a tabular form.

## Study Area
This project gathered data about the Upper Chattahoochee watershed. The watershed intersects many different counties and the Chattahoochee river is the main tributary river to Lake Lanier as well as a major fresh water source to Georgia, Alabama, and Florida. 

### Counties Involved 
Union, Towns, Lumpkin, White, Habersham, Hall, Dawson, Forsyth, Gwinnett, Fulton, Cherokee, Cobb, and Dekalb 

### Study Area Map
The map pictured below is not a completly depiction of the study area, It represents the upper section of the Upper Chattahoochee watershed above the Buford Dam and doesn't display some of the lower counties in the study area.  

![StudyAreaMap](https://raw.githubusercontent.com/jzmiller1/squish/master/readme_static/UpperUpperChattahoocheeCountiesLandcover_170k_ANSID.jpg)

## Data Sources

### National Land Cover Dataset

#### Source Summary 
The National Land Cover Database (NLCD) provides spatial and descriptive data for the different types of land cover from Landsat satellite imagery. The NLCD data products are created by the Multi-Resolution Land Characteristics (MRLC) Consortium, which is a partnership of Federal agencies led through the U.S Geological Survey. The NLCD has collected national land cover data for the years of 1992, 2001, 2006, and 2011. The NLCD data products are available for free download with no charge to the public through the MRLC website. The primary objective of the MRLC NLCD is to ultimately provide our nation with complete and consistent information on the land cover. The MRLC-NLCD releases the national land cover datasets usually on a 5-year product period. For more information on the MRLC Consortium and the federal agencies involved visit the [main website](http://www.mrlc.gov/).
   
#### Data Structure
The NLCD is in raster format collected through the Landsat satellite and is downloaded through the MRLC- NLCD, led by the U.S Geological Survey. The NLCD data is downloaded as a zip file for each desired year, which will need to be extracted. The NLCD data for the entire U.S in the years of 2001, 2006, and 2011 all use the same Land Cover Class Descriptions, which is modified from the Anderson Land Cover Classification System. The attribute table for each of the NLCD year datasets has a Value field (Land Cover Class Code Value), a Count field (how many pixels represent that land cover), a Land Cover Class field (text description of the land cover), and more. This data collected by Landsat has a spatial resolution of 30 meters. For more detailed descriptions on the dataset, the data download comes with a metadata file for each NLCD year. 

#### Spatial Information
The map projection used for the NLCD data (2001, 2006, and 2011) is the Albers Conical Equal Area. The horizontal datum used is the North American Datum of 1983 and the ellipsoid used is the Geodetic Reference System 80. 

#### What is avaliable in the Loader
The NLCD data for 2001, 2006, and 2011 was successful when clipping the NLCD data for the entire U.S to the HUC12 Upper Chattahoochee watershed boundary. The loader also tabulates the land cover data for all 2001, 2006, and 2011 datasets to the different sets of data within the area of interest for this project, such as the counties, census tracts, block groups, blocks, and the smaller hydrologic unit codes. 
   
### National Hydrology Dataset

####Source Summary
  -Where: NHD(regular)data downloaded from: (nhd.usgs.gov/data.html)
  
  -Last modified: Thursday, 18-Aug-2016 11:08:23 EDT

---

####Data Structure: 
point, line, and polygon shape files

---

####Spatial Information

##### Extent
- The Extent of the NHD/NHD+ information contains all the watersheds in each state of the USA, including the Phillipines, Guam, Puerto Rico, Northern Mariana, and American Samoa. For the NHD/NHD+ data, the NED (National Elevation Dataset) Snapshots were used to formulate the HUC (Hydrologic Unit Code) data. The HUC data measures watershed boundaries within the domestic continental united states. For this particular project, we separated the HUC 8, 10, and 12 data for The Upper Chattahoochee area.


##### Geographic Coordinate System
- We transformed the NDH/NHD+ data from GCS_North_American_1983 (SRID:4269) to NAD 1983 (SRID:6630). It was necessary for us to transform the projection to this coordinate system in order to more accurately represent the spatial features of the hydrology dataset to the census, tranformation, and NLCD data.
  
---

####*What is available in the Loader*

-NHDArea.shx

-NHDFlowline.shx

-NHDLine.shx

-NHDPoint.shx

-NHDPointEventFC.shx

-WBDHU2.shx

-WBDHU4.shx

-WBDHU6.shx

-WBDHU8.shx

-WBDHU10.shx

-WBDHU12.shx

-WBDLine.shx


---

####Directions for future work
- *NHD+ data download from*: (https://www.epa.gov/waterdata/nhdplus-national-data)
- Download NHD extracts by state; high resolution; GDB: NHD_H_13_GDB.zip:
- Download NHD extracts by state; high resolution; Shape: NHD_H_13_Shape.zip:
- (Download one file at a time)
  + NHDplusV21_nationaldata
  + _GageInfo_05.7z
  + _GageLoc_05.7z
  + _Gage_Smooth_01.7z
  + _NationalCat_02.7z
  + _National_Seamless_Geodatabase_02.7z
  + _V1_To_V2_Crosswalk_01.7z
  + _WBDSnapshot_FileGDB_08.7c
  + _WDBSnapshot_Shapefile_08.7z
  + NHD_H_13_GDB.gdb :arrow_right: WBD :arrow_right: WBDHU8, WBDHU10, WDBHU12
  + NHD_H_13_GDB.gdb :arrow_right: Hydrography :arrow_right: NHDFlowline, NHDWaterbody
  + NHDPlusV21_National_Seamless.gdb :arrow_right: NHDEvents :arrow_right: Gage
  + NHDPlusV21_National_Seamless.gdb :arrow_right: NHDPlusCatchment :arrow_right: Catchment
  + NHDPlusV21_National_Seamless.gdb :arrow_right: NHDSnapshot :arrow_right: NHDFlowline_Network, NHDWaterbody
- In the file “WBDHU8” select by attributes name: Upper Chattahoochee
- Create feature layer from selection 
*All other files listed above were clipped to this new feature layer using the clip analysis tool*
- In all the HUC files (8,10, & 12) create and or delete fields needed to match all attributes fields in each attribute table (ex: delete field “NONCOUNTRR_K” and “NONCONTRA_A” from HUC_12; Because these fields are empty) 
  + (Create a field called HUC: String because some of the counts start at zero which is why one can’t use short or long integer, from all the files) (Replaced the Huc number field for each file with the new field HUC)
####Adding to pgadmin(iii)
  - Create a database with a name associated with watershed for future reference. 
  - Create extension postgis in the sql pane for a spatial feature reference function.
  - Go to the plugins option at the top of the program window.  
    + Select the second option (postGIS shapefile to DBF loader 2.2) 
    + Navigate to the U: shared drive. Locate the file path.
    + Add the shape files. 
    *The simplest way is to add the files instead of appending any to each other. Use the srid # 4269 for each shape file. However, if one wanted to add the huc files into one table for easy callment in the future that is an option.  There are several ways to organize the data into tables this is  the users choice.*
  - Transform Projection in pgadmin(iii).

### Transportation Data

#### Source Summary
Our data came exclusively from the Government’s Census Bureau Topologically Integrated Geographic Encoding and Referencing Road (TIGER) database.

* TIGER Site
  * Data Structure
    * 13 Counties that are included in our area of study, the Upper Chattahoochee watershed
      * Cherokee
      * Cobb
      * Dawson
      * Dekalb
      * Forsyth
      * Fulton
      * Gwinnett
      * Habersham
      * Hall
      * Lumpkin
      * Towns
      * Union
      * White
    * 2 Sets of the data by year
      * 2011
      * 2016
    * What does it include?
      * The Tiger road data is a line shape file that includes the street name, road type and the state/county’s ID.
      * Contains Primary and Secondary road data
    * Spatial Information
      * North American Datum of 1983
      * Uses this Geographical Coordinate system for all data
    * Python Loader
      * We edited the loader to work for transportation data
* ### Import Census Tracts to Database ###
  * roads_2011 = 'data\\transportation_2011.shp'
  * roads_2016 = 'data\\transportation_2016.shp'
      * cursor.execute("""CREATE EXTENSION IF NOT EXISTS pgrouting;""")
* Set the correct spatial reference system for our data (Code too long to post)
* shp2pgsql_command = " ".join([shp2pgsql_path, "-c", "-s 94269", '-W latin1', os.path.join(BASE_DIR, roads_2011), "roads2011"])
  * Upon running, it crashed and did not work
      * This is due to the size of the data, using a smaller data set proved to work fine
      * QGIS /pgRouting Procedure
  * 1.	Open PostGIS Shapefile and DBF loader 2.2
  * 2.	Set the SRID as 4269 and import the road data to the database
  * 3.	Create postgis and pgrouting extension to the database. 
      * CREATE EXTENSION postgis;
      * CREATE EXTENSION pgrouting;
  * 4.	Add ‘source’ and ‘target’ column and create topology for the road data
      * ALTER TABLE roaddata ADD COLUMN 'source' integer;
      * ALTER TABLE roaddata ADD COLUMN 'target' integer;
  * SELECT pgr_createTopology('roaddata', 0.00001, 'geom', 'gid');
  * 5.	Fails to create topology
  * 6.	Attempt pgRouting via QGIS pgRouting extension tested on two random points and it fails to return a value
* PSQL Procedure
  * 1.	Zip the road data and upload to dropbox 
  * 2.	Dl link: https://www.dropbox.com/s/ji9y05ae92y5f2y/2016%2B2011.zip?dl=0
  * 3.	Go to the console window on the Vultr machine and log in
  * 4.	In the command line, install the “unzip” apt
  * 5.	cmd: sudo apt-get install unzip
  * 6.	Install the “postgis” apt
  * 7.	cmd: sudo apt-get install postgis
  * 8.	Download the road data from dropbox
  * 9.	cmd: wget “https://www.dropbox.com/s/ji9y05ae92y5f2y/2016%2B2011.zip?dl=0”
  * 10.	Unzip the road data
  * 11.	cmd: unzip 2016+2011.zip?dl=0 –d /home
  * 12.	Create an output folder and name it “output_20XX”
  * 13.	cmd: cd /home
      * cd /home/2011
      * mkdir output_2011
  * 14.	Change directory to the folder where the .shp file locate (hint. Use “ls”)
  * 15.	Use “shp2pgsql” tool that is initially installed with pgrouting to convert .shp file to a table (.sql file)
  * 16.	cmd: shp2pgsql tl_2011_13057_roads.shp cherokee > /home/2011/output_2011/Cherokee_2011_13057_roads.sql
  * 17.	Change directory back to root
  * 18.	Now, we are going to import the .sql file into the database
  * 19.	cmd: su postgres
  * 20.	In pgadmin III, create a new database (In our case, we named it “project”)
  * 21.	In the command line, type:
      * psql
      * /connect project
      * create extension postgis;
      * create extension pgrouting;
  * 22.	Import the .sql file to the database
  * 23.	cmd: psql –h 45.32.210.174 –d project –U postgres –f /home/2011/output_2011/Cherokee_2011_13057_roads.sql
* ArcMap Procedure
  * 1.	Open the Road Data up into ArcMap(One county at a time)
  * 2.	Run the “Rebuild Connectivity” tool
  * 3.	Fill out the pop up window accordingly for the dataset(Spatial Reference System, buffer size, etc)
  * 4.	Run the tool, it finishes successfully
  * 5.	Go back to QGIS and run pgRouting on the corrected shapefile, it still fails
  * 6.	Test multiple other parameters in the “Rebuild Connectivity” tool, continues to fail after each attempt
* Georgia Clearing House Procedure(Successful Attempt)
  * 1.	Download Data from Georgia Clearing House
  * 2.	Open QGIS
  * 3.	Import the road data and export that by eliminating the Z-dimension (Elevation) and M-dimension(Route) data.
  * 4.	Open PostGIS Shapefile and DBF loader 2.2 in pgAdminIII
  * 5.	Set the SRID as 4269 and import the road data to the database
  * 6.	Create postgis and pgrouting extension to the database. 
      * CREATE EXTENSION postgis;
      * CREATE EXTENSION pgrouting;
  * 7.	Add ‘source’ and ‘target’ column and create topology for the road data
      * ALTER TABLE roaddata ADD COLUMN 'source' integer;
      * ALTER TABLE roaddata ADD COLUMN 'target' integer;
      * SELECT pgr_createTopology('roaddata', 0.00001, 'geom', 'gid');
  * 8.	Run the query that returns a set of pgr_costResult (seq, id1, id2, cost) rows, that make up a path
  * 9.	In order to visualize the result, we can display the path in QGIS. Open QGIS and connect to the Postgres database
  * 10.	Open the DB Manager and open the SQL window
  * 11.	Run the query and export the visual representation in QGIS
      * SELECT seq, id1 AS node,id2 AS edge, cost, geom FROM pgr_dijkstra('
      SELECT gid AS id, 
          source, 
          target, 
          minute::float8 AS cost
   FROM roaddata',
117232,
90731,
false,
false) as route JOIN roaddata on roaddata.gid = route.id2
* Conclusion
  * For the future, don’t use Tiger data for any pgRouting or Network Analysis, the data set is fragmented and does not work properly, even after spatial correction.
      * Fragmentation refers to the issue that the line features that represent the roads within the shapefile do not connect with one another at a vertex where a connection should be present.
      * Georgia Clearing House data did not have this issue and worked correctly using the exact same procedure. 
•	Georgia Clearing House

## Loader
In order to get the different types of data sets that were gathered into the repository we had to create a database and insert the data using a loader. 
The loader was a Python program created to automate the process.

### Python Module Used
The loader program, rundown.py, utilizes several Python libraries.  The standard library modules utilized by rundown.py include the os and sub-process modules which 
require no installation outside of the installation of Python itself.  The loader also requires the third party Python library psycopg2 to connect and interface 
with PostgreSQL databases. [Psycopg2](https://pypi.python.org/pypi/psycopg2) is available for download or installation through the pip package manager and the Python Package Index.  

The final modules used by the loader are the nlcd and secret modules created specifically for this project.  The nlcd module has Python 
data structures containing data from the MRLC's NLCD and the secret module is a module that is not tracked in the project repository that contains sensitive information
that should not be shared on GitHub such as the database username, password and host.

### How the Loader Works
+ The tools used in order for the loader to properly run are raster2pgsql and shp2pgsql. 
+ The loader creates a database which is automatically loaded into PGAdminIII. 
+ The loader also connects to the basic directory(BASE_DIR) which contains the data intended for the repository.
+ In order to streamline the uploading process, the loader will automatically drop database files when new ones are edited or created. 
+ The loader spatially enables the database by inserting the correct SRIDs which is used by the NLCD raster data and the spatial census data.
+ The SRIDs or spatial referance idenifier used are 96630 for the NLCD raster data and 102003 for the spatial census data. 
+ SRIDs obtained from cross-referancing the projection in the metadata with online references(spatialreferances.org). 
+ The loader also enables the extension for the UUID or Universally Unique Identifier [uuid-ossp].


## Database Setup/Schema
After the loader has finished, the database will contain 30 different tables.  The breakdown of those tables is as follows:
  + blckgroup_1990 - polygon information for the 1990 block groups in the census data
  + blckgroup_2000 - polygon information for the 2000 block groups in the census data
  + blckgroup_2010 - polygon information for the 2010 block groups in the census data
  + block_1990 - polygon information for the 1990 blocks in the census data
  + block_2000 - polygon information for the 2000 blocks in the census data
  + block_2010 - polygon information for the 2010 blocks in the census data
  + catchments - polygon information for the catchments in the NHD Plus data
  + codebook - table that lists some of the column titles in the census data and explains their meanings
  + county_1990 - polygon information for the 1990 counties in the census data
  + county_1990_pop - tabular information for the 1990 county populations in the census data
  + county_2000 - polygon information for the 2000 counties in the census data
  + county_2010 - polygon information for the 2010 counties in the census data
  + gages - point information for the gages in the NHD Plus data
  + huc - polygon information for the HUC-8, HUC-10, and HUC-12 in one table for the NHD data
  + nhd_flowlines - line information for streams in the NHD data
  + nhd_waterbodies - polygon information for the waterbodies in the NHD data
  + nhdp_flowlines - line information for streams in the NHD Plus data
  + nhdp_waterbodies - polygon information for the waterbodies in the NHD Plus data
  + nlcd2001 - raster information for the 2001 NLCD
  + nlcd2006 - raster information for the 2006 NLCD
  + nlcd2011 - raster information for the 2011 NLCD
  + spatial_ref_sys - table that lists all spatial referenced available in the creation of a spatial database
  + tabulation_huc - tabulation data calculated from the huc table compared to the NLCD tables land cover codes
  + tabulation_huc_generalized - tabulation data calculated from the huc table compared to the NLCD tables land cover types
  + tabulation_tract - tabulation data calculated from the tract tables compared to the NLCD tables land cover codes
  + tabulation_tract_generalized - tabulation data calculated from the tract tables compared to the NLCD tables land cover types
  + tract_1990 - polygon information for the 1990 tracts in the census data
  + tract_1990_pop - tabular information for the 1990 tracts in the census data
  + tract_2000 - polygon information for the 2000 tracts in the census data
  + tract_2010 - polygon information for the 2010 tracts in the census data
