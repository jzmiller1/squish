/* Base16 Atelier Heath Light - Theme */
/* by Bram de Haan (http://atelierbram.github.io/syntax-highlighting/atelier-schemes/heath) */
/* Original Base16 color scheme by Chris Kempson (https://github.com/chriskempson/base16) */
/* https://github.com/jmblog/color-themes-for-highlightjs */

/* Atelier Heath Light Comment */
.hljs-comment,
.hljs-title {
  color: #776977;
}

/* Atelier Heath Light Red */
.hljs-variable,
.hljs-attribute,
.hljs-tag,
.hljs-regexp,
.ruby .hljs-constant,
.xml .hljs-tag .hljs-title,
.xml .hljs-pi,
.xml .hljs-doctype,
.html .hljs-doctype,
.css .hljs-id,
.css .hljs-class,
.css .hljs-pseudo {
  color: #ca402b;
}

/* Atelier Heath Light Orange */
.hljs-number,
.hljs-preprocessor,
.hljs-pragma,
.hljs-built_in,
.hljs-literal,
.hljs-params,
.hljs-constant {
  color: #a65926;
}

/* Atelier Heath Light Yellow */
.hljs-ruby .hljs-class .hljs-title,
.css .hljs-rules .hljs-attribute {
  color: #bb8a35;
}

/* Atelier Heath Light Green */
.hljs-string,
.hljs-value,
.hljs-inheritance,
.hljs-header,
.ruby .hljs-symbol,
.xml .hljs-cdata {
  color: #379a37;
}

/* Atelier Heath Light Aqua */
.css .hljs-hexcolor {
  color: #159393;
}

/* Atelier Heath Light Blue */
.hljs-function,
.python .hljs-decorator,
.python .hljs-title,
.ruby .hljs-function .hljs-title,
.ruby .hljs-title .hljs-keyword,
.perl .hljs-sub,
.javascript .hljs-title,
.coffeescript .hljs-title {
  color: #516aec;
}

/* Atelier Heath Light Purple */
.hljs-keyword,
.javascript .hljs-function {
  color: #7b59c0;
}

.hljs {
  display: block;
  overflow-x: auto;
  background: #f7f3f7;
  color: #695d69;
  padding: 0.5em;
  -webkit-text-size-adjust: none;
}

.coffeescript .javascript,
.javascript .xml,
.tex .hljs-formula,
.xml .javascript,
.xml .vbscript,
.xml .css,
.xml .hljs-cdata {
  opacity: 0.5;
}




# squish
GISC 4011K class project

## _National Hydrology Dataset_


###Where: NHD(regular)data downloaded from: nhd.usgs.gov/data.html
###When Updated: Last modified: Thursday, 18-Aug-2016 11:08:23 EDT
###Structure of the data: point, line, and polygon shape files:

---

####Raw Data:
1. Downloaded NHD extracts by state; high resolution; GDB: NHD_H_13_GDB.zip:
2. Downloaded NHD extracts by state; high resolution; Shape: NHD_H_13_Shape.zip:
3. *NHD+ data downloaded from*: (https://www.epa.gov/waterdata/nhdplus-national-data)
4. (Download one file at a time)
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

#####Unzip data somewhere safe
In ArcMap added this data:
1.*Geographic Coordinate System: GCS_North_American_1983 (SRID:4269)*
  + NHD_H_13_GDB.gdb  WBDWBDHU8,WBDHU10, WDBHU12
  + NHD_H_13_GDB.gdbHydrographyNHDFlowline, NHDWaterbody
  + NHDPlusV21_National_Seamless.gdbNHDEventsGage
  + NHDPlusV21_National_Seamless.gdbNHDPlusCatchmentCatchment
  + NHDPlusV21_National_Seamless.gdbNHDSnapshotNHDFlowline_Network, NHDWaterbody
  
---

######Editing within ArcMap:
1. In the file “WBDHU8” Selected by attributes Name: Upper Chattahoochee
2. Create feature layer from selection 
All other files listed above were clipped to this new feature layer using the clip analysis tool
3. In all the Huc files (8,10, &12) create and or delete fields needed to match all attributes fields in each attribute table (ex: delete field “NONCOUNTRR_K” and “NONCONTRA_A” from Huc_12; Because these fields are empty) 
  + (Create a field called HUC: String because some of the counts start at zero which is why one can’t use short or long integer, from all the files) (Replaced the Huc number field for each file with the new field huc)

---

######Adding to pgadmin(iii):
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
 


