"""
Module de chargement des données pour le réseau électrique.

Ce module gère le chargement des données statiques et temporelles 
du réseau électrique d'Hydro-Québec. Il prend en charge la lecture des fichiers CSV
pour la configuration du réseau et les séries temporelles de production/consommation.

Functions:
    load_network_data: Charge les données statiques du réseau.
    load_timeseries_data: Charge les données temporelles.

Classes:
    NetworkDataLoader: Classe principale pour le chargement des données.
    DataLoadError: Exception personnalisée pour les erreurs de chargement.

Example:
    >>> from network.utils import NetworkDataLoader
    >>> loader = NetworkDataLoader()
    >>> network_data = loader.load_network_data()
    >>> timeseries_data = loader.load_timeseries_data('2024')

Notes:
    Les données doivent suivre la structure suivante :
    - data/
        ├── regions/
        │   └── buses.csv         # Points de connexion du réseau
        │
        ├── topology/
        │   ├── lines/
        │   │   ├── line_types.csv    # Types de lignes standard
        │   │   └── lines.csv         # Lignes de transmission
        │   │
        │   └── centrales/
        │       ├── carriers.csv      # Types de production
        │       └── generators.csv     # Caractéristiques des centrales
        │
        └── timeseries/
            └── 2024/
                ├── generation/
                │   └── generators-p_max_pu.csv  # Production maximale par unité
                └── loads-p_set.csv              # Profils de charge

Contributeurs : Yanis Aksas (yanis.aksas@polymtl.ca)
                Add Contributor here
"""

import pypsa
import pandas as pd
from pathlib import Path
from typing import Optional


class DataLoadError(Exception):
    """Exception levée lors d'erreurs de chargement des données."""
    pass


class NetworkDataLoader:
    """
    Gestionnaire de chargement des données du réseau.

    Cette classe utilise les fonctionnalités natives de PyPSA pour charger
    les données du réseau à partir des fichiers CSV.

    Attributes:
        data_dir (Path): Chemin vers le répertoire des données
    """

    def __init__(self, data_dir: str = "data"):
        """
        Initialise le chargeur de données.

        Args:
            data_dir: Chemin vers le répertoire des données.
                Defaults to "data".

        Raises:
            DataLoadError: Si le répertoire n'existe pas.
        """
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise DataLoadError(f"Le répertoire {data_dir} n'existe pas")

    def load_network_data(self) -> pypsa.Network:
        """
        Charge les données statiques du réseau.

        Cette méthode charge la topologie du réseau (buses, lignes, générateurs)
        en utilisant la fonction native de PyPSA import_from_csv_folder.

        Returns:
            pypsa.Network: Réseau PyPSA configuré avec les données statiques.

        Raises:
            DataLoadError: Si les données sont inaccessibles ou mal formatées.
        """
        try:
            network = pypsa.Network()
            
            # Chargement des données régionales (buses)
            buses_df = pd.read_csv(self.data_dir / "regions" / "buses.csv")
            buses_df = buses_df.set_index('name')
            for idx, row in buses_df.iterrows():
                network.add("Bus", name=idx, **row.to_dict())
            
            # Chargement des lignes
            line_types_df = pd.read_csv(self.data_dir / "topology" / "lines" / "line_types.csv")
            line_types_df = line_types_df.set_index('name')
            for idx, row in line_types_df.iterrows():
                network.add("LineType", name=idx, **row.to_dict())
            
            lines_df = pd.read_csv(self.data_dir / "topology" / "lines" / "lines.csv")
            lines_df = lines_df.set_index('name')
            for idx, row in lines_df.iterrows():
                network.add("Line", name=idx, **row.to_dict())

            # Chargement des générateurs 
            carriers_df = pd.read_csv(self.data_dir / "topology" / "centrales" / "carriers.csv")
            carriers_df = carriers_df.set_index('name')
            for idx, row in carriers_df.iterrows():
                network.add("Carrier", name=idx, **row.to_dict())

            generators_df = pd.read_csv(self.data_dir / "topology" / "centrales" / "generators.csv")
            generators_df = generators_df.set_index('name')
            for idx, row in generators_df.iterrows():
                network.add("Generator", name=idx, **row.to_dict())
            
            return network
            
        except Exception as e:
            raise DataLoadError(f"Erreur lors du chargement des données: {str(e)}")

    def load_timeseries_data(self, 
                           network: pypsa.Network,
                           year: str,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> pypsa.Network:
        """
        Ajoute les données temporelles au réseau.

        Args:
            network: Réseau PyPSA à compléter avec les données temporelles
            year: Année des données (ex: '2024')
            start_date: Date de début au format 'YYYY-MM-DD' (optionnel)
            end_date: Date de fin au format 'YYYY-MM-DD' (optionnel)

        Returns:
            pypsa.Network: Réseau avec les données temporelles ajoutées

        Raises:
            DataLoadError: Si les données sont inaccessibles ou mal formatées
        """
        try:
            # Chargement des séries temporelles pour les charges (loads)
            loads_path = self.data_dir / "timeseries" / year / "loads-p_set.csv"
            loads_df = pd.read_csv(loads_path, index_col=0, parse_dates=True)
            network.loads_t.p_set = loads_df

            
            # Chargement des coûts marginaux des générateurs
            gen_path = self.data_dir / "timeseries" / year / "generation" / "generators-marginal_cost.csv"
            gen_df = pd.read_csv(gen_path, index_col=0, parse_dates=True)
            network.generators_t.marginal_cost = gen_df
            
            # Définition des snapshots
            network.set_snapshots(loads_df.index)
            
            return network
            
        except Exception as e:
            raise DataLoadError(
                f"Erreur lors du chargement des données temporelles: {str(e)}"
            )