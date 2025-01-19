def ajouter_lignes(network):

    lignes = [
        ("Montreal", "LaGrande-2"),
        ("Brisay","Laforge-2"),
        ("Laforge-2","Laforge-1"),
        ("Laforge-1","LaGrande-4"),
        ("LaGrande-4","LaGrande-2"),
    ]

    for i, (bus0, bus1) in enumerate(lignes, start=1):
        network.add("Line",f"Ligne{i}",bus0=bus0,bus1=bus1,x=0.33,r=0.01)
