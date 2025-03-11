import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Charger le fichier Shapefile des MRC
shapefile_path = "officiel/data/MRC_GROUPE_9/base_mrc_database.shp"
gdf_mrc = gpd.read_file(shapefile_path)

# Charger le fichier CSV contenant les lignes de transmission
lines_file_path = "officiel/data/topology/lignes_quebec.csv"
df_lines = pd.read_csv(lines_file_path)

# Charger le fichier CSV contenant les noms des MRC
mrc_names_file_path = "officiel/data/MRC_GROUPE_9/coordonnees_MRC.csv"
df_mrc_names = pd.read_csv(mrc_names_file_path)

# Créer un dictionnaire de mappage des ID des MRC aux noms des MRC
mrc_names_dict = pd.Series(df_mrc_names.CDNAME.values, index=df_mrc_names.ID).to_dict()

# Filtrer les points valides (ceux qui ont des coordonnées non nulles)
df_lines_valid = df_lines.dropna(subset=['latitude_starting', 'longitude_starting', 'latitude_ending', 'longitude_ending'])

# Convertir les points valides en GeoDataFrame
geometry_starting = [Point(xy) for xy in zip(df_lines_valid['longitude_starting'], df_lines_valid['latitude_starting'])]
geometry_ending = [Point(xy) for xy in zip(df_lines_valid['longitude_ending'], df_lines_valid['latitude_ending'])]

gdf_points_starting = gpd.GeoDataFrame(df_lines_valid, geometry=geometry_starting)
gdf_points_ending = gpd.GeoDataFrame(df_lines_valid, geometry=geometry_ending)

# Effectuer une jointure spatiale pour trouver à quelle MRC appartiennent les points de départ et de fin
gdf_points_starting_in_mrc = gpd.sjoin(gdf_points_starting, gdf_mrc, how="inner", predicate="within")
gdf_points_ending_in_mrc = gpd.sjoin(gdf_points_ending, gdf_mrc, how="inner", predicate="within")

# Filtrer les points qui n'appartiennent pas aux MRC
gdf_points_starting_not_in_mrc = gdf_points_starting[~gdf_points_starting.index.isin(gdf_points_starting_in_mrc.index)]
gdf_points_ending_not_in_mrc = gdf_points_ending[~gdf_points_ending.index.isin(gdf_points_ending_in_mrc.index)]

# Afficher les points qui n'appartiennent pas aux MRC avec leurs coordonnées
print("\nPoints de départ qui n'appartiennent pas aux MRC:")
pd.set_option('display.max_rows', None)
print(gdf_points_starting_not_in_mrc[['network_node_name_starting', 'latitude_starting', 'longitude_starting']])

print("\nPoints de fin qui n'appartiennent pas aux MRC:")
print(gdf_points_ending_not_in_mrc[['network_node_name_ending', 'latitude_ending', 'longitude_ending']])

# Grouper les points par MRC et afficher les résultats
mrc_points_starting = gdf_points_starting_in_mrc.groupby('index_right').apply(lambda x: x[['network_node_name_starting', 'latitude_starting', 'longitude_starting']].to_dict(orient='records'))
mrc_points_ending = gdf_points_ending_in_mrc.groupby('index_right').apply(lambda x: x[['network_node_name_ending', 'latitude_ending', 'longitude_ending']].to_dict(orient='records'))

print("\nListe des MRC et des points de départ qui les composent:")
for mrc_id, points in mrc_points_starting.items():
    mrc_name = mrc_names_dict.get(mrc_id)  # Utiliser le dictionnaire pour obtenir le nom du MRC
    print(f"\n{mrc_id}, {mrc_name}")
    for point in points:
        print(f"  Point: {point['network_node_name_starting']}, Latitude: {point['latitude_starting']}, Longitude: {point['longitude_starting']}")

print("\nListe des MRC et des points de fin qui les composent:")
for mrc_id, points in mrc_points_ending.items():
    mrc_name = mrc_names_dict.get(mrc_id)  # Utiliser le dictionnaire pour obtenir le nom du MRC
    print(f"\n{mrc_id}, {mrc_name}")
    for point in points:
        print(f"  Point: {point['network_node_name_ending']}, Latitude: {point['latitude_ending']}, Longitude: {point['longitude_ending']}")

# Identifier les points qui sont à la fois des points de départ et des points de fin
common_points = pd.merge(gdf_points_starting_in_mrc, gdf_points_ending_in_mrc, left_on=['network_node_name_starting', 'latitude_starting', 'longitude_starting'], right_on=['network_node_name_ending', 'latitude_ending', 'longitude_ending'])

# Définir la colonne de géométrie active pour common_points
common_points = gpd.GeoDataFrame(common_points, geometry='geometry_x')

# Tracer les points sur la carte des MRC
fig, ax = plt.subplots(figsize=(10, 8))
gdf_mrc.plot(ax=ax, edgecolor="black", cmap="viridis")

# Points de départ (bleu)
gdf_points_starting_in_mrc.plot(ax=ax, color='blue', markersize=5, label='Starting Points')

# Points de fin (rouge)
gdf_points_ending_in_mrc.plot(ax=ax, color='red', markersize=5, label='Ending Points')

# Points de départ et de fin (vert)
common_points.plot(ax=ax, color='green', markersize=5, label='Starting and Ending Points')

ax.set_title("Carte des MRC avec Points de Départ et de Fin")
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()