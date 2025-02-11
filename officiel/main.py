"""
Script principal pour tester le chargement des données du réseau électrique.

Ce script utilise le NetworkDataLoader pour charger et valider les données
du réseau d'Hydro-Québec, puis affiche quelques informations de base.
"""

from utils import NetworkDataLoader, DataLoadError, NetworkValidator
import sys
from pathlib import Path


def print_network_info(network):
    """Affiche les informations détaillées du réseau."""
    print("\n=== Informations du réseau ===")
    print(f"Nombre de bus: {len(network.buses)}")
    print(f"Nombre de lignes: {len(network.lines)}")
    print(f"Nombre de générateurs: {len(network.generators)}")
    print(f"Nombre de types de lignes: {len(network.line_types)}")
    print(f"Nombre de carriers: {len(network.carriers)}")
    
    print("\n=== Types de générateurs ===")
    print("Générateurs pilotables:")
    pilotables = network.generators[network.generators.type == 'pilotable']
    print(pilotables.groupby('carrier').p_nom.sum())
    
    print("\nGénérateurs non pilotables:")
    non_pilotables = network.generators[network.generators.type == 'non_pilotable'] 
    print(non_pilotables.groupby('carrier').p_nom.sum())
    
    if hasattr(network, 'snapshots'):
        print("\n=== Période temporelle ===")
        print(f"Début: {network.snapshots[0]}")
        print(f"Fin: {network.snapshots[-1]}")
        print(f"Nombre de pas de temps: {len(network.snapshots)}")


def main():
    """Fonction principale."""
    try:
        # Initialisation du loader
        loader = NetworkDataLoader()
        
        # Chargement des données statiques
        print("\nChargement des données statiques...")
        network = loader.load_network_data()
        print("✓ Données statiques chargées avec succès")

        # Affichage des informations statiques
        print_network_info(network)

        # Chargement des données temporelles
        print("\nChargement des données temporelles pour 2024...")
        network = loader.load_timeseries_data(network, '2024')
        print("✓ Données temporelles chargées")

        # Affichage des informations complètes
        print_network_info(network)

        # Test d'accès aux données temporelles
        print("\n=== Vérification des données temporelles ===")
        print("\nProfils de charge (premiers points):")
        print(network.loads_t.p_set.head())
        
        print("\nCoûts marginaux des générateurs pilotables (premiers points):")
        print(network.generators_t.marginal_cost.head())
        
        print("\nProduction maximale des générateurs non pilotables (premiers points):")
        print(network.generators_t.p_max_pu.head())

        return 0

    except DataLoadError as e:
        print(f"\nErreur lors du chargement des données: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\nErreur inattendue: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())