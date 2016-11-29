
# squish
GISC 4011K class project

## _National Hydrology Dataset_ :ocean:


###Where: NHD(regular)data downloaded from: nhd.usgs.gov/data.html
###When Updated: Last modified: Thursday, 18-Aug-2016 11:08:23 EDT
###Structure of the data: point, line, and polygon shape files:

---

####Raw Data
- Downloaded NHD extracts by state; high resolution; GDB: NHD_H_13_GDB.zip:
- Downloaded NHD extracts by state; high resolution; Shape: NHD_H_13_Shape.zip:
- *NHD+ data downloaded from*: (https://www.epa.gov/waterdata/nhdplus-national-data)
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
  
---

####Unzip data :globe_with_meridians:
In ArcMap add this data:
- *Geographic Coordinate System: GCS_North_American_1983 (SRID:4269)* 
  + NHD_H_13_GDB.gdb :arrow_right: WBD :arrow_right: WBDHU8, WBDHU10, WDBHU12
  + NHD_H_13_GDB.gdb :arrow_right: Hydrography :arrow_right: NHDFlowline, NHDWaterbody
  + NHDPlusV21_National_Seamless.gdb :arrow_right: NHDEvents :arrow_right: Gage
  + NHDPlusV21_National_Seamless.gdb :arrow_right: NHDPlusCatchment :arrow_right: Catchment
  + NHDPlusV21_National_Seamless.gdb :arrow_right: NHDSnapshot :arrow_right: NHDFlowline_Network, NHDWaterbody
  
---

####Editing within ArcMap :computer:
- In the file “WBDHU8” Selected by attributes Name: Upper Chattahoochee
- Create feature layer from selection 
All other files listed above were clipped to this new feature layer using the clip analysis tool
- In all the Huc files (8,10, &12) create and or delete fields needed to match all attributes fields in each attribute table (ex: delete field “NONCOUNTRR_K” and “NONCONTRA_A” from Huc_12; Because these fields are empty) 
  + (Create a field called HUC: String because some of the counts start at zero which is why one can’t use short or long integer, from all the files) (Replaced the Huc number field for each file with the new field huc)

---

####Adding to pgadmin(iii) :elephant:
  - Create a database with a name associated with watershed for future reference. Create extension postgis in the sql pane for a spatial feature reference function.
  - Go to the plugins option at the top of the program window.  
    + Select the second option (postGIS shapefile to DBF loader 2.2) 
    + Navigate to the U: shared drive. Locate the file path: 
    ![alt text](https://github.com/valerieclark95/NHDpictures/blob/master/nhd1.png "file path")
    + Add the shape files. 
    *The simplest way is to add the files instead of appending any to each other. Use the srid # 4269 for each shape file. However, if one wanted to add the huc files into one table for easy callment in the future that is an option.  There are several ways to organize the data into tables this is  the users choice.*
  - Transform Projection in pgadmin(iii):
We need to transform the watershed srid 4269 projection to the NLCD coordinate system(nad 1983, srid, 6630) for simpilicity so that all the  class projects data are in the same projection.  Code used to change the coordinate system is placed in the U drive.
![alt text](https://github.com/valerieclark95/NHDpictures/blob/master/nhd2.png "sql file path")
 


