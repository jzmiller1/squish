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
### Census Data
#### Source Summary
The census is an official survey issued by the United States Census Bureau which is a part of the U.S. Department of Commerce and overseen by the Economics and Statistics Administration. This survey is issued every 10 years with the purpose of counting every resident in the United States in order to properly determine the number of seats each state has in the U.S. House of Representatives and fairly distribute federal funds to local communities. This process is written into the constitution under Article 1, Section 2. 
We gathered our data directly from the National Historical Geographic Information System (NHGIS) which is one of the world’s largest collections of statistical provides open source cumulative census data and provides GIS-compatible boundary data files of the United States from 1790 to the present. This project was started and is managed by the Minnesota Population Center at the University of Minnesota. NHGIS now not only includes census data, but data from other national surveys as well.  NHGIS is one of the world’s largest collections of statistical provides open source cumulative census data and GIS-compatible boundary data files of the United States from 1790 to the present.
#### Data structure 
Since census data is collected on a regular basis for the entire nation is it is available on several different scales, the largest being the national level. Below the national level are the regional and then divisions levels. Below them is the state level. The state level can be further divided by school or congressional districts, urban growth areas, state legislative districts, and public use microdata areas. The next level below state is counties which can be further divided as well. The county subgroups include voting districts, traffic analysis zones, and county subdivisions. Below Counties is the census tract, block groups, and census block levels. While census tracts and the levels above it stay the same geographically, blocks change. Once a block becomes too populated it will be divided into two blocks. The purpose of this is to keep each block of roughly the same population.  
Since the census is collected every ten years, the data is available for each round of collection as well. For the NHGIS project they started formatting all standard census data from the 1990 census. Data is available for prior years, but it is limited.  
#### Tabular Data 
The tabular data available includes educational information, household per capita income, housing values, population, poverty level, and transportation time for work for the years 1990, 2000, and 2010 for Cherokee, Cobb, Dawson, DeKalb, Forsyth, Fulton, Gwinnett, Habersham, Hall, Lumpkin, Towns, Union, and White County. Not all data was available at every level however and more detail is given below. 
##### Education	
Household per capita income is an average based on the previous year. For the years 1990 and 2010 the data is available by county, tract, and block group. For 2000 the data is available for county and tract only. Additionally, some of this data is associated with the region and division numbers.Housing values are an average for the given breakdown. For 1990 the data is available by block, block group, tract, and county. For 2000 it is available in county and tract. For 2010 the data is available for block group, tract, and county. 
##### Population 
The population data obtained from the USGS is based on the US Census and includes information on the District of Columbia, Alaska, Hawaii, and Puerto Ricco and is based on the previous year's census. Population data for this project was downloaded from NHGIS for the years 1990, 2000, and 2010. These files contain information on the year filed, the county, tract, block group, and block that the population data is referring to.
##### Poverty Level Status
Travel time to work is slightly more complex. The population considered in these calculations were workers over the age of 16 who did not work at home. The travel times is then broken down into intervals of 5 minutes. Our first interval (E3W001) includes the number of workers who traveled less than 5 minutes to work. Our second interval (E3W002) includes the number of workers who traveled 10 to 14 minutes to get to work. This pattern continues all the way to our last interval (E3W012) which includes the number of workers who traveled 90 minutes or more for work. This data is available for 1990 and 2010 by block group, tract, and county. For 2000 this data is available by county and tract only. 
We included some information that was not necessary for our project, such as the region and division numbers which would be the same for all of our data. However, this data was already available in the downloaded tables and we thought there was no harm in keeping it. If in the future the project were to be expanded in any way to other areas, this would make it easy to relate back to these higher levels of the census hierarchy.  
One thing I notice when working with this data was that for the years 2010 and 1990 a more detailed break of the data was available (block group, block). However, for 2000 the data was often only found by county and tract. The only possible reason I could think of for doing this is so that we would be able to show a more detailed view of change over the whole time span. Organizing data by block and block group for 2000 as well may have been too tedious and time consuming for its usefulness. 
#### Spatial Data
The spatial information used for this project was downloaded from NHGIS included county, tract, block group, and block boundaries for the years 2000, 2009, and 2010. They are in the format of shapefiles (.shp) and are identified by the survey year. 
##### Extent
The shapefiles for the 1990 Georgia counties, block groups, blocks, and tracts were downloaded from NHGIS and added to ArcMap. Next, to create a shapefile that only contains counties in the HUC 6 study area, the following select by attribute was created and saved as a shapefile: 

"STATENAM" = 'Georgia' AND ("NAHGISNAM"= 'Cherokee' OR " NAHGISNAM "='Cobb' OR " NAHGISNAM "='Dawson' OR " NAHGISNAM "='DeKalb' OR " NAHGISNAM "= 'Forsyth' OR " NAHGISNAM "= 'Fulton' OR " NAHGISNAM "= 'Gwinnett' OR " NAHGISNAM "= 'Habersham' OR " NAHGISNAM "= 'Hall' OR " NAHGISNAM "= 'Lumpkin' OR " NAHGISNAM "= 'Towns' OR " NAHGISNAM "= 'Union' Or " NAHGISNAM "= 'White');

To create appropriate tract, block group, and block study areas, a select by location query was executed on each of the Georgia tract using the “select features from” method on the 1990 Georgia tract layer with the source layer set as the newly created HUC 6 shapefile using the “intersect the source layer feature” spatial selection method. A shapefile was created from this selection yielding a shapefile that contains all of the tracts in the HUC 6 watershed. This process was executed on all of the Georgia tracts, blocks, and block groups shapefiles for the years 1990, 2000, and 2010. 

##### Coordinate System
NHGIS shapefiles use Esri’s USA Contiguous Albers Equal Area Conic projection. This projection is useful as it preserves area for small regions. It uses two standard parallels in order to reduce distortion and is best suited for landmasses extending in an east-to west orientation. The meridians are equally spaces in this conic projection and are straight lines that come to a single common point. Parallels are unequally spaces concentric circles whose spacing decreases toward the poles. Shape along the standard parallels is accurate and all areas are proportional.
#### What is Available in the Loader
A shapefile for each Georgia county HUC 6 tract, block group, and block for the years 1990, 2000, and 2010 is in the loader. Population information for the study area is the only tabular data available in the loader due to variations in the tables. 


### National Land Cover Dataset

#### Source Summary 
The National Land Cover Database (NLCD) provides spatial and descriptive data for the different types of land cover from Landsat satellite imagery. The NLCD data products are created by the Multi-Resolution Land Characteristics (MRLC) Consortium, which is a partnership of Federal agencies led through the U.S Geological Survey. The NLCD has collected national land cover data for the years of 1992, 2001, 2006, and 2011. The NLCD data products are available for free download with no charge to the public through the MRLC website. The primary objective of the MRLC NLCD is to ultimately provide our nation with complete and consistent information on the land cover. The MRLC-NLCD releases the national land cover datasets usually on a 5-year product period. For more information on the MRLC Consortium and the federal agencies involved visit the [main website](http://www.mrlc.gov/).
   
#### Data Structure
The NLCD is in raster format collected through the Landsat satellite and is downloaded through the MRLC- NLCD, led by the U.S Geological Survey. The NLCD data is downloaded as a zip file for each desired year, which will need to be extracted. The NLCD data for the entire U.S in the years of 2001, 2006, and 2011 all use the same Land Cover Class Descriptions, which is modified from the Anderson Land Cover Classification System. The attribute table for each of the NLCD year datasets has a Value field (Land Cover Class Code Value), a Count field (how many pixels represent that land cover), a Land Cover Class field (text description of the land cover), and more. This data collected by Landsat has a spatial resolution of 30 meters. For more detailed descriptions on the dataset, the data download comes with a metadata file for each NLCD year. 

#### Spatial Information
##### Extent
The NLCD data once downloaded has all the national land cover data for the whole United States. Before using the Loader, the NLCD data for each of the years (2001, 2006, 2011) needs to be clipped to the area of interest boundary, which is the HUC12 Upper Chattahoochee watershed. 
##### Coordinate System
The map projection used for the NLCD data (2001, 2006, and 2011) is the Albers Conical Equal Area. The horizontal datum used is the North American Datum of 1983 and the ellipsoid used is the Geodetic Reference System 80. 

#### What is available in the Loader
The land cover data for 2001, 2006, and 2011 was successful when loading the clipped NLCD data for the HUC12 Upper Chattahoochee watershed boundary. The loader also tabulates the land cover data for all 2001, 2006, and 2011 datasets to the different sets of data within the area of interest for this project, such as the counties, census tracts, block groups, blocks, and the smaller hydrologic unit codes. 
   
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
  
### Applications 
#### 1 
A community or government entity may be interested in keeping a certian natural landcover percentage for a watershed. 
This could be because to problems with runoff, sedimentary pollution, and low water quality due to  water not being able to sink into the soil prorperly. 
One could not only see the percentage of land cover per HUC boundary, but also the correlation between the natural land cover and growth of population 
and human infastructure. They might compare transportation data with the NLCD sets to see if percentage of area that roads occupy is acceptable for the 
health of the environment. 
Entities that might interested in this website: Government(Local, State, and Federal), Land developers, city planners, the EPA, watch dog adgencies and Universities
If a watch dog adgency was very ambitious they might compare developement and land cover data to habitats of endangered species and streams that are 303 D(extremely
polluted)listed by the EPA. 
