#import geopandas as gpd
#import matplotlib.pyplot as plt

# Charger le fichier Shapefile
#shapefile_path = "officiel/data/MRC_GROUPE_9/base_mrc_database.shp"
#gdf = gpd.read_file(shapefile_path)

# Afficher un aperçu des données
#print(gdf.head())

# Créer la carte
#fig, ax = plt.subplots(figsize=(10, 8))
#gdf.plot(ax=ax, edgecolor="black", cmap="viridis") 
#ax.set_title("Carte des MRC", fontsize=14)

#plt.show()

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Charger le fichier Shapefile des MRC
shapefile_path = "officiel/data/MRC_GROUPE_9/base_mrc_database.shp"
gdf_mrc = gpd.read_file(shapefile_path)

# Afficher toutes les données des MRC
print(gdf_mrc)

# Charger le fichier CSV contenant les points
csv_file_path = "officiel/data/topology/geolocated_nodes.csv"
df_points = pd.read_csv(csv_file_path)

# Filtrer les points où used_as_end est True, used_as_start est True, et les deux
df_points_end = df_points[df_points['used_as_end'] == True]
df_points_start = df_points[df_points['used_as_start'] == True]
df_points_both = df_points[(df_points['used_as_end'] == True) & (df_points['used_as_start'] == True)]

# Convertir les points filtrés en GeoDataFrame
geometry_end = [Point(xy) for xy in zip(df_points_end['longitude'], df_points_end['latitude'])]
geometry_start = [Point(xy) for xy in zip(df_points_start['longitude'], df_points_start['latitude'])]
geometry_both = [Point(xy) for xy in zip(df_points_both['longitude'], df_points_both['latitude'])]

gdf_points_end = gpd.GeoDataFrame(df_points_end, geometry=geometry_end)
gdf_points_start = gpd.GeoDataFrame(df_points_start, geometry=geometry_start)
gdf_points_both = gpd.GeoDataFrame(df_points_both, geometry=geometry_both)

# Effectuer une jointure spatiale pour trouver à quelle MRC appartiennent les points
gdf_points_in_mrc_end = gpd.sjoin(gdf_points_end, gdf_mrc, how="left", predicate="within")
gdf_points_in_mrc_start = gpd.sjoin(gdf_points_start, gdf_mrc, how="left", predicate="within")
gdf_points_in_mrc_both = gpd.sjoin(gdf_points_both, gdf_mrc, how="left", predicate="within")

# Afficher toutes les données des résultats dans le prompt
print("Points utilisés comme fin:")
print(gdf_points_in_mrc_end)
print("Points utilisés comme début:")
print(gdf_points_in_mrc_start)
print("Points utilisés comme début et fin:")
print(gdf_points_in_mrc_both)

# Créer la carte
fig, ax = plt.subplots(figsize=(10, 8))
gdf_mrc.plot(ax=ax, edgecolor="black", cmap="viridis")
gdf_points_end.plot(ax=ax, color="red", markersize=5, label="End")
gdf_points_start.plot(ax=ax, color="blue", markersize=5, label="Start")
gdf_points_both.plot(ax=ax, color="green", markersize=5, label="Start and End")
ax.set_title("Carte des MRC avec Points", fontsize=14)
plt.legend()

plt.show()

# Grouper les points par MRC et calculer la somme des demandes
grouped_end = gdf_points_in_mrc_end.groupby('index_right').size()
grouped_start = gdf_points_in_mrc_start.groupby('index_right').size()
grouped_both = gdf_points_in_mrc_both.groupby('index_right').size()

# Afficher la liste des MRC et des points qui les composent
print("\nListe des MRC et des points qui les composent:")
for mrc_id, count in grouped_end.items():
    print(f"MRC ID: {mrc_id}, Points utilisés comme fin: {count}")
for mrc_id, count in grouped_start.items():
    print(f"MRC ID: {mrc_id}, Points utilisés comme début: {count}")
for mrc_id, count in grouped_both.items():
    print(f"MRC ID: {mrc_id}, Points utilisés comme début et fin: {count}")