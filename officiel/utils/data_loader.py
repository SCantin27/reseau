"""
Module de chargement des données pour le réseau électrique.

Ce module gère le chargement des données statiques et temporelles 
du réseau électrique d'Hydro-Québec. Il prend en charge la lecture des fichiers JSON
de configuration du réseau et des séries temporelles de production/consommation.

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
    Les données doivent suivre une structure spécifique :
    - data/network/ : Données statiques (plants.json, lines.json, etc.)
    - data/timeseries/2024/ : Données temporelles par année
        - generation/
            - hydro.json
            - eolien.json
            - solar.json
            - thermal.json
        - consumption.json

Contributeurs : Yanis Aksas (yanis.aksas@polymtl.ca)
                Add Contributor here
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Union, Optional
from dataclasses import dataclass


class DataLoadError(Exception):
    """Exception levée lors d'erreurs de chargement des données."""
    pass


@dataclass
class NetworkData:
    """
    Structure de données pour les composants statiques du réseau.

    Attributes:
        plants (Dict): Données des centrales électriques
        lines (Dict): Données des lignes de transmission
        substations (Dict): Données des postes électriques
    """
    plants: Dict
    lines: Dict
    substations: Dict


class NetworkDataLoader:
    """
    Gestionnaire de chargement des données du réseau.

    Cette classe s'occupe de charger et valider les données nécessaires
    à la construction et à la simulation du réseau électrique.

    Attributes:
        data_dir (Path): Chemin vers le répertoire des données
        network_dir (Path): Sous-répertoire des données statiques
        timeseries_dir (Path): Sous-répertoire des données temporelles
    """

    def __init__(self, data_dir: str = "data"):
        """
        Initialise le chargeur de données.

        Args:
            data_dir: Chemin vers le répertoire des données.
                Defaults to "data".

        Raises:
            DataLoadError: Si le répertoire n'existe pas ou n'est pas accessible.
        """
        self.data_dir = Path(data_dir)
        self.network_dir = self.data_dir / "network"
        self.timeseries_dir = self.data_dir / "timeseries"

        if not self.data_dir.exists():
            raise DataLoadError(f"Le répertoire {data_dir} n'existe pas")

    def load_network_data(self) -> NetworkData:
        """
        Charge les données statiques du réseau.

        Returns:
            NetworkData: Structure contenant les données du réseau.

        Raises:
            DataLoadError: Si un fichier est manquant ou mal formaté.
        """
        try:
            plants = self._load_json_file(self.network_dir / "plants.json")
            lines = self._load_json_file(self.network_dir / "lines.json")
            substations = self._load_json_file(self.network_dir / "substations.json")
            
            return NetworkData(
                plants=plants,
                lines=lines,
                substations=substations
            )
        except Exception as e:
            raise DataLoadError(f"Erreur lors du chargement des données: {str(e)}")

    def load_timeseries_data(self, 
                           year: str,
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> Dict:
        """
        Charge les données temporelles pour une année spécifique.

        Args:
            year: Année des données (ex: '2024')
            start_date: Date de début au format 'YYYY-MM-DD' (optionnel)
            end_date: Date de fin au format 'YYYY-MM-DD' (optionnel)

        Returns:
            Dict contenant les données temporelles de production et consommation

        Raises:
            DataLoadError: Si les données sont inaccessibles ou mal formatées
        """
        year_dir = self.timeseries_dir / year
        try:
            # Chargement des données de production par type
            generation = {}
            for gen_type in ['hydro', 'eolien', 'solar', 'thermal']:
                file_path = year_dir / "generation" / f"{gen_type}.json"
                generation[gen_type] = self._load_json_file(file_path)

            # Chargement des données de consommation (à confirmer avec l'équipe 09)
            consumption = self._load_json_file(year_dir / "consumption.json")

            # Filtrage temporel si nécessaire
            if start_date and end_date:
                # Logique de filtrage à implémenter
                pass

            return {
                "generation": generation,
                "consumption": consumption
            }

        except Exception as e:
            raise DataLoadError(
                f"Erreur lors du chargement des données temporelles: {str(e)}"
            )

    def _load_json_file(self, file_path: Path) -> Dict:
        """
        Charge un fichier JSON.

        Args:
            file_path: Chemin vers le fichier JSON

        Returns:
            Dict: Contenu du fichier JSON

        Raises:
            DataLoadError: Si le fichier est inaccessible ou mal formaté
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise DataLoadError(f"Fichier non trouvé: {file_path}")
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Erreur de format JSON dans {file_path}: {str(e)}")