import geopandas, pandas

boundary = geopandas.read_file("C:/Users/LENOVO/Documents/GIS_DATASETS/mwi_admin2_em.shp")

gdf = geopandas.GeoDataFrame(boundary)
gdf.to_file("mw_admin.geojson", driver = 'GeoJSON')