# squish
GISC 4011K class project

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
