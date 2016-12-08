# squish
GISC 4011K class project

##Upper Chattahoochee Watershed

####Abstract:
   The goal of this project is to transfer Census, National Land Cover Database (NLCD), National Hydrographic Dataset (NHD) and Transport data pertaining to the Upper Chattahoochee Watershed and  to arrange them into a systematic form. Sources for the data were extracted from the National Historical Geographic Information System(NHGIS) database, NLCD hosted by the Multi-Resolution Land Characteristics (MRLC) database, NHD, and the TIGER database from the Census website. The methods include acquiring the data, clipping the raster data, using the Windows command line to covert the files from raster to SQL, in which presented problems for the transportation data. The SQL files are loaded into the database, using a python database loader which will push the data into a tabular form.

## Data Sources

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
  
---

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
