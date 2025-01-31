"""
Module de gestion des calculs de flux de puissance.

Ce module fournit des fonctions utilitaires pour exécuter et analyser
les calculs de flux de puissance sur le réseau d'Hydro-Québec en utilisant PyPSA.

Example:
    >>> from network.core import NetworkBuilder, run_power_flow
    >>> builder = NetworkBuilder()
    >>> network = builder.build_network()
    >>> success = run_power_flow(network)
    >>> print(network.lines_t.p0)  # Affiche les flux de puissance

Contributeurs : Yanis Aksas (yanis.aksas@polymtl.ca)
                Add Contributor here
"""

import pypsa
import pandas as pd
from typing import Optional, Tuple, Dict


def run_power_flow(network: pypsa.Network,
                  mode: str = "dc",
                  snapshot: Optional[str] = None) -> bool:
    """
    Exécute un calcul de flux de puissance sur le réseau.

    Args:
        network (pypsa.Network): Réseau à analyser
        mode (str, optional): "ac" ou "dc". Defaults to "dc".
        snapshot (str, optional): Instant spécifique. Defaults to None.

    Returns:
        bool: True si le calcul a convergé, False sinon

    Note:
        Les résultats sont directement stockés dans l'objet network :
        - network.lines_t.p0 : Flux de puissance
        - network.lines_t.loading : Chargement des lignes
        - network.buses_t.v_ang : Angles de tension (mode AC)
        - network.buses_t.v_mag_pu : Magnitudes de tension (mode AC)
    """
    try:
        if mode == "ac":
            return network.pf(snapshots=snapshot)
        else:
            return network.lpf(snapshots=snapshot)
    except Exception as e:
        print(f"Erreur lors du calcul de flux de puissance : {str(e)}")
        return False


def get_line_loading(network: pypsa.Network) -> pd.Series:
    """
    Retourne le chargement des lignes en pourcentage.

    Args:
        network (pypsa.Network): Réseau analysé

    Returns:
        pd.Series: Chargement de chaque ligne en %
    """
    return network.lines_t.loading * 100


def get_critical_lines(network: pypsa.Network, threshold: float = 90.0) -> Dict[str, float]:
    """
    Identifie les lignes fortement chargées.

    Args:
        network (pypsa.Network): Réseau analysé
        threshold (float): Seuil de chargement en %. Defaults to 90.0.

    Returns:
        Dict[str, float]: Lignes dépassant le seuil avec leur chargement
    """
    loading = get_line_loading(network)
    return {line: load for line, load in loading.items() 
            if load > threshold}