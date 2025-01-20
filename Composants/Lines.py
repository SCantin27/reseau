def ajouter_lignes(network):

    #Define point A to point B of every lines
    lignes = [
        ("LaGrande-2", "Montreal"),
        ("Brisay","Laforge-2"),
        ("Laforge-2","Laforge-1"),
        ("Laforge-1","LaGrande-4"),
        ("LaGrande-4","LaGrande-2"),
    ]

    # Define a custom line type (Not working currently)
    ligne_735kV = {
        "r": 0.01,        # Resistance in Ohms/km
        "x": 0.33,        # Reactance in Ohms/km
        "g": 0.0,         # Shunt conductance in Siemmens/km
        "b": 0.01*10e-6,  # Shunt susceptance in Siemmens/km
        "s_nom": 10,      # Nominal power in MVA.
    }

    # Add the custom line type to the network
    network.line_types.loc["ligne_735kV"] = ligne_735kV
 
    #Add all the lines defined in 'lignes' to the network, using the 735kV type
    for i, (bus0, bus1) in enumerate(lignes, start=1):
        network.add("Line",f"Ligne{i}",bus0=bus0,bus1=bus1,lenght = 100, x=0.33, r=0.01, g=0, b=10e-6)
