"""
Script principal pour tester le chargement des données du réseau électrique.

Ce script utilise le NetworkDataLoader pour charger et valider les données
du réseau d'Hydro-Québec, puis affiche quelques informations de base.
"""

from utils import NetworkDataLoader, DataLoadError, NetworkValidator
import sys
from pathlib import Path


def print_network_info(network):
    """Affiche les informations principales du réseau."""
    print("\n=== Informations du réseau ===")
    print(f"Nombre de bus: {len(network.buses)}")
    print(f"Nombre de lignes: {len(network.lines)}")
    print(f"Nombre de générateurs: {len(network.generators)}")
    
    print("\n=== Types de générateurs ===")
    print(network.generators.groupby('carrier').p_nom.sum())
    
    if hasattr(network, 'snapshots'):
        print("\n=== Période temporelle ===")
        print(f"Début: {network.snapshots[0]}")
        print(f"Fin: {network.snapshots[-1]}")
        print(f"Nombre de pas de temps: {len(network.snapshots)}")


def main():
    """Fonction principale."""
    try:
        # Initialisation du loader et du validateur
        loader = NetworkDataLoader()
        validator = NetworkValidator()

        # Chargement des données statiques
        print("\nChargement des données statiques...")
        network = loader.load_network_data()
        print("✓ Données statiques chargées")

        # Affichage des informations statiques
        print_network_info(network)

        # Chargement des données temporelles
        print("\nChargement des données temporelles pour 2024...")
        network = loader.load_timeseries_data(network, '2024')
        print("✓ Données temporelles chargées")

        # Validation du réseau complet
        print("\nValidation du réseau...")
        if validator.validate_network(network):
            print("✓ Réseau validé avec succès")

        # Affichage des informations complètes
        print_network_info(network)

        # Test d'accès aux données temporelles
        print("\n=== Test d'accès aux données temporelles ===")
        print("\nProfil de charge (premiers points):")
        print(network.loads_t.p_set.head())

        return 0

    except DataLoadError as e:
        print(f"\nErreur lors du chargement des données: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\nErreur inattendue: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())