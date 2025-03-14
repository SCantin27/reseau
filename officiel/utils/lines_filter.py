"""
Module lines_filter.

Ce module gère le filtrage et la géolocalisation des lignes de transmission.
Il utilise les fonctions de lecture de fichiers Excel/CSV pour extraire
des informations sur les lignes et les nœuds du réseau électrique.

Functions:
    filter_quebec_lines: Filtre les lignes de transmission du Québec.
    get_unique_nodes: Récupère tous les nœuds uniques.
    geolocate_nodes: Géolocalise les nœuds en utilisant l'API Nominatim.

Classes:
    LineFilter: Classe principale pour le filtrage et la géolocalisation.

Example:
    >>> from network.utils import LineFilter
    >>> line_filter = LineFilter()
    >>> line_filter.filter_quebec_lines('input.xlsx', 'quebec_lines.csv')
    >>> line_filter.get_unique_nodes('quebec_lines.csv', 'unique_nodes.csv')
    >>> line_filter.geolocate_nodes('unique_nodes.csv', 'geolocated_nodes.csv')
"""

import pandas as pd
import requests
import time
import os

class LineFilter:
    def __init__(self):
        self.column_names = [
            'transmission_line_id', 'transmission_circuit_id', 'owner', 'province',
            'operating_region', 'number_of_circuits', 'current_type',
            'line_segment_length_km', 'line_segment_length_mi', 'line_length_km',
            'line_length_mi', 'voltage', 'reactance', 'ttc_summer', 'ttc_winter',
            'network_node_name_starting', 'network_node_code_starting',
            'network_node_name_ending', 'network_node_code_ending', 'notes'
        ]

    def _read_excel_file(self, input_file):
        """
        Méthode pour lire et préparer le fichier Excel
        """
        try:
            # Lire le fichier Excel
            df = pd.read_excel(input_file, engine='openpyxl')
            
            # Si toutes les données sont dans une seule colonne
            if len(df.columns) == 1:
                # Diviser chaque ligne en utilisant la virgule
                df = pd.DataFrame([x.split(',') for x in df[df.columns[0]]])
                # Ignorer la première ligne (qui contient les en-têtes) et utiliser nos noms de colonnes
                df = df.iloc[1:].reset_index(drop=True)
                df.columns = self.column_names
            
            # Nettoyer les guillemets des valeurs
            df = df.apply(lambda x: x.str.strip('"') if x.dtype == "object" else x)
            
            return df
            
        except Exception as e:
            print(f"Une erreur est survenue lors de la lecture du fichier : {str(e)}")
            return None

    def filter_quebec_lines(self, input_file, output_file):
        """
        Filtre les lignes de transmission du Québec à partir d'un fichier Excel
        et les exporte dans un fichier CSV.
        
        Args:
            input_file (str): Chemin du fichier Excel d'entrée
            output_file (str): Chemin du fichier CSV de sortie
        """
        try:
            df = self._read_excel_file(input_file)
            if df is None:
                return
            
            # Filtrer les lignes du Québec
            quebec_df = df[df['province'] == 'QC']
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Exporter en CSV
            quebec_df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"Nombre de lignes pour le Québec : {len(quebec_df)}")
            print(f"Fichier sauvegardé : {output_file}")
            
        except Exception as e:
            print(f"Une erreur est survenue : {str(e)}")
            if 'df' in locals():
                print("Colonnes dans le fichier :", df.columns.tolist())

    def get_unique_nodes(self, input_file, output_file):
        """
        Récupère tous les noms de nœuds uniques (starting et ending) du réseau
        et les sauvegarde dans un fichier CSV.
    
        Args:
            input_file (str): Chemin du fichier d'entrée (CSV ou Excel)
            output_file (str): Chemin du fichier CSV de sortie
        """
        try:
            # Lire le fichier selon son extension
            if input_file.endswith('.csv'):
                df = pd.read_csv(input_file)
            else:
                df = self._read_excel_file(input_file)
            
            if df is None:
                return
        
            # Récupérer tous les nœuds de départ et d'arrivée
            starting_nodes = df['network_node_name_starting'].unique()
            ending_nodes = df['network_node_name_ending'].unique()
        
            # Créer un DataFrame avec tous les nœuds uniques
            all_nodes = pd.DataFrame({
                'node_name': sorted(list(set(starting_nodes) | set(ending_nodes))),
            })
        
            # Ajouter des colonnes indiquant si le nœud est utilisé comme départ et/ou arrivée
            all_nodes['used_as_start'] = all_nodes['node_name'].isin(starting_nodes)
            all_nodes['used_as_end'] = all_nodes['node_name'].isin(ending_nodes)
        
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
            all_nodes.to_csv(output_file, index=False, encoding='utf-8')
        
            print(f"Nombre total de nœuds uniques : {len(all_nodes)}")
            print(f"Fichier sauvegardé : {output_file}")
        

            stats = {
                'total_nodes': len(all_nodes),
                'starting_nodes': sum(all_nodes['used_as_start']),
                'ending_nodes': sum(all_nodes['used_as_end']),
                'both_nodes': sum(all_nodes['used_as_start'] & all_nodes['used_as_end'])
            }
        
            #print(f"Nœuds utilisés comme départ : {stats['starting_nodes']}")
            #print(f"Nœuds utilisés comme arrivée : {stats['ending_nodes']}")
            #print(f"Nœuds utilisés comme départ et arrivée : {stats['both_nodes']}")
        
        except Exception as e:
            print(f"Une erreur est survenue lors de la récupération des nœuds : {str(e)}")
    
    def geolocate_nodes(self, input_nodes_file, output_geolocated_file):
        """
        Géolocalise les nœuds à partir de leurs noms en utilisant l'API Nominatim.
        
        Args:
            input_nodes_file (str): Chemin du fichier CSV contenant les nœuds
            output_geolocated_file (str): Chemin du fichier CSV de sortie avec les coordonnées
        """
        
        try:
            df = pd.read_csv(input_nodes_file)
            
            # Préparer les colonnes pour les coordonnées
            df['latitude'] = None
            df['longitude'] = None
            
            # API Nominatim
            base_url = "https://nominatim.openstreetmap.org/search"
            headers = {
                'User-Agent': 'PIV',  # Identifiant Nominatim
                'Accept': 'application/json'
            }
            
            print(f"Début de la géolocalisation de {len(df)} nœuds...")
            
            # Parcourir chaque nœud
            for index, row in df.iterrows():
                node_name = row['node_name']
                
                # Préparer les paramètres de la requête
                params = {
                    'q':node_name + ", Québec",
                    'format': 'json',               
                    'limit': 1  # On prend que le premier résultat
                }
                
                try:
                    # Faire la requête à l'API
                    response = requests.get(base_url, params=params, headers=headers)
                    
                    if response.status_code == 200:
                        results = response.json()
                        
                        if results:
                            # Stocker les coordonnées
                            df.at[index, 'latitude'] = float(results[0]['lat'])
                            df.at[index, 'longitude'] = float(results[0]['lon'])
                            
                            print(f"Nœud {node_name} géolocalisé : {results[0]['lat']}, {results[0]['lon']}")
                        else:
                            print(f"Aucun résultat trouvé pour le nœud {node_name}")
                    
                    else:
                        print(f"Erreur lors de la requête pour {node_name}: {response.status_code}")
                    
                    # Attendre entre chaque requête
                    time.sleep(0.25)
                    
                except Exception as e:
                    print(f"Erreur lors de la géolocalisation de {node_name}: {str(e)}")
                    continue
            
            total_nodes = len(df)
            geolocated_nodes = df['latitude'].notna().sum()
            
            #print(f"Nœuds géolocalisés : {geolocated_nodes}")
            #print(f"Pourcentage de réussite : {(geolocated_nodes/total_nodes)*100:.2f}%")
            
            os.makedirs(os.path.dirname(output_geolocated_file), exist_ok=True)
            
            # Sauvegarder le résultat
            df.to_csv(output_geolocated_file, index=False, encoding='utf-8')
            print(f"\nRésultats sauvegardés dans : {output_geolocated_file}")
            
        except Exception as e:
            print(f"Une erreur est survenue : {str(e)}")

    def fill_missing_coordinates(self, input_geolocated_file, output_filled_file):
            """
            Remplit les coordonnées manquantes en utilisant la moyenne des coordonnées
            du point précédent et du point suivant dans la liste.
            
            Args:
                input_geolocated_file (str): Chemin du fichier CSV contenant les nœuds géolocalisés
                output_filled_file (str): Chemin du fichier CSV de sortie avec les coordonnées remplies
            """
            try:
                df = pd.read_csv(input_geolocated_file)
                
                # Parcourir chaque ligne pour trouver les coordonnées manquantes
                for index, row in df.iterrows():
                    if pd.isna(row['latitude']) or pd.isna(row['longitude']):
                        prev_index = None
                        for i in range(index - 1, -1, -1):
                            if not pd.isna(df.at[i, 'latitude']) and not pd.isna(df.at[i, 'longitude']):
                                prev_index = i
                                break
                        # Trouver le point suivant avec des coordonnées valides
                        next_index = None
                        for i in range(index + 1, len(df)):
                            if not pd.isna(df.at[i, 'latitude']) and not pd.isna(df.at[i, 'longitude']):
                                next_index = i
                                break
                        if prev_index is not None and next_index is not None:
                            prev_lat = df.at[prev_index, 'latitude']
                            prev_lon = df.at[prev_index, 'longitude']
                            next_lat = df.at[next_index, 'latitude']
                            next_lon = df.at[next_index, 'longitude']
                            
                            if not pd.isna(prev_lat) and not pd.isna(next_lat):
                                df.at[index, 'latitude'] = (prev_lat + next_lat) / 2
                            if not pd.isna(prev_lon) and not pd.isna(next_lon):
                                df.at[index, 'longitude'] = (prev_lon + next_lon) / 2
                
                os.makedirs(os.path.dirname(output_filled_file), exist_ok=True)
                
                # Sauvegarder le résultat
                df.to_csv(output_filled_file, index=False, encoding='utf-8')
                print(f"Résultats avec coordonnées remplies sauvegardés dans : {output_filled_file}")
                
            except Exception as e:
                print(f"Une erreur est survenue lors du remplissage des coordonnées : {str(e)}")



    def add_coordinates_to_lines(self, lines_file, geolocated_nodes_file):
        """
        Ajoute les coordonnées géographiques aux villes dans le fichier des lignes de transmission.
        
        Args:
            lines_file (str): Chemin du fichier CSV contenant les lignes de transmission
            geolocated_nodes_file (str): Chemin du fichier CSV contenant les nœuds géolocalisés
        """
        try:
            # Lire les fichiers CSV
            lines_df = pd.read_csv(lines_file)
            geolocated_nodes_df = pd.read_csv(geolocated_nodes_file)
            
            # Créer un dictionnaire pour les coordonnées géographiques
            coordinates_dict = geolocated_nodes_df.set_index('node_name')[['latitude', 'longitude']].to_dict('index')
            
            # Ajouter ou mettre à jour les colonnes pour les coordonnées géographiques
            lines_df['latitude_starting'] = lines_df['network_node_name_starting'].map(lambda x: coordinates_dict.get(x, {}).get('latitude'))
            lines_df['longitude_starting'] = lines_df['network_node_name_starting'].map(lambda x: coordinates_dict.get(x, {}).get('longitude'))
            lines_df['latitude_ending'] = lines_df['network_node_name_ending'].map(lambda x: coordinates_dict.get(x, {}).get('latitude'))
            lines_df['longitude_ending'] = lines_df['network_node_name_ending'].map(lambda x: coordinates_dict.get(x, {}).get('longitude'))
            
            # Réorganiser les colonnes pour insérer les coordonnées juste après les noms des villes
            cols = list(lines_df.columns)
            starting_index = cols.index('network_node_name_starting')
            ending_index = cols.index('network_node_name_ending') 
            cols.insert(starting_index + 1, cols.pop(cols.index('latitude_starting')))
            cols.insert(starting_index + 2, cols.pop(cols.index('longitude_starting')))
            cols.insert(ending_index + 1, cols.pop(cols.index('latitude_ending')))
            cols.insert(ending_index + 2, cols.pop(cols.index('longitude_ending')))
            lines_df = lines_df[cols]
            
            # Sauvegarder le résultat en écrasant le fichier d'entrée
            lines_df.to_csv(lines_file, index=False, encoding='utf-8')
            print(f"Résultats avec coordonnées ajoutées sauvegardés dans : {lines_file}")
            
        except Exception as e:
            print(f"Une erreur est survenue lors de l'ajout des coordonnées : {str(e)}")



    def extract_lines(self, input_file, output_file):
        """
        Extrait les informations des lignes de transmission du fichier lignes_quebec.csv
        et les sauvegarde dans le fichier lines.csv avec les colonnes spécifiées.
        
        Args:
            input_file (str): Chemin du fichier CSV d'entrée (lignes_quebec.csv)
            output_file (str): Chemin du fichier CSV de sortie (lines.csv)
        """
        try:
            df = pd.read_csv(input_file)
            
            # Initialiser une liste pour stocker les nouvelles lignes
            new_lines = []
            
            for index, row in df.iterrows():
                name = f"L{index + 1:04d}"
                bus0 = row['network_node_name_starting']
                bus1 = row['network_node_name_ending']
                type_line = f"{row['voltage']}kV_line"
                length = row['line_segment_length_km']
                capital_cost = length * 1000  # Estimation du coût
                s_nom = 10000 + (index % 2) * 10000  # Alternance entre 10000 et 20000
                
                new_lines.append([name, bus0, bus1, type_line, length, capital_cost, s_nom])
            
            # Créer un DataFrame avec les nouvelles lignes
            new_lines_df = pd.DataFrame(new_lines, columns=['name', 'bus0', 'bus1', 'type', 'length', 'capital_cost', 's_nom'])
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Sauvegarder en CSV
            new_lines_df.to_csv(output_file, index=False, encoding='utf-8')
            
            print(f"Nombre de lignes extraites : {len(new_lines_df)}")
            print(f"Fichier sauvegardé : {output_file}")
            
        except Exception as e:
            print(f"Une erreur est survenue lors de l'extraction des lignes : {str(e)}")

# ajouter module 

    # Chemins des fichiers


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Chemins des fichiers
    input_file = os.path.join(project_root, "data", "topology", "transmission_lines.xlsx")
    output_quebec_file = os.path.join(project_root, "data", "topology", "lignes_quebec.csv")
    output_nodes_file = os.path.join(project_root, "data", "topology", "unique_nodes.csv")
    output_geolocated_file = os.path.join(project_root, "data", "topology", "geolocated_nodes.csv")
    output_filled_file = os.path.join(project_root, "data", "topology", "filled_geolocated_nodes.csv")
    input_file = os.path.join(project_root, "data", "topology", "lignes_quebec.csv")
    output_lines_file = os.path.join(project_root, "data", "topology", "lines", "lines.csv")
    
    line_filter = LineFilter()
    
    # # Exécuter le filtrage des lignes du Québec
    # line_filter.filter_quebec_lines(input_file, output_quebec_file)
    
    # # Exporter les nœuds uniques
    # line_filter.get_unique_nodes(output_quebec_file, output_nodes_file)

    # line_filter.geolocate_nodes(output_nodes_file, output_geolocated_file )

    # Extraire les lignes et sauvegarder dans lines.csv
    line_filter.extract_lines(input_file, output_lines_file)

    # Remplir les coordonnées manquantes
    #line_filter.fill_missing_coordinates(output_geolocated_file, output_filled_file)

    # Ajouter les coordonnées géographiques aux lignes de transmission
   #line_filter.add_coordinates_to_lines(output_quebec_file, output_filled_file)