def ajouter_lignes(network):
    from Fonctions.Length_calculator import haversine

    

    # Define point A to point B for every line
    lignes = [
        ("LaGrande-2", "Montreal"),
        ("Brisay", "Laforge-2"),
        ("Laforge-2", "Laforge-1"),
        ("Laforge-1", "LaGrande-4"),
        ("LaGrande-4", "LaGrande-2"),
    ]

    # Define a custom line type (No need to pass the dictionary here, use it by name later)
    ligne_735kV = {
        "f_nom" : 50,
        "r_per_length" : 0.01,
        "x_per_length" : 0.33,
        "c_per_length" : 8,
        "i_nom" : 0.6,
        "mounting" : "ol",
        "cross_section" : 500,
        "reference" : "none"
    }

    # Add the custom line type to the network
    network.line_types.loc["ligne_735kV"] = ligne_735kV


    # Verify if the line type has been added correctly
    print("Line types in the network after addition:")
    print(network.line_types)


    # Add all the lines defined in 'lignes' to the network, using the 735kV type
    for i, (bus0, bus1) in enumerate(lignes, start=1):
        # Calculate the distance between the two buses using the haversine function
        haversine_length = haversine(
            network.buses.loc[bus0, 'y'], network.buses.loc[bus0, 'x'],
            network.buses.loc[bus1, 'y'], network.buses.loc[bus1, 'x']
        )

        # Add the line to the network using the custom line type by name
        network.add(
            "Line", f"Ligne{i}",
            bus0=bus0, bus1=bus1,
            type="ligne_735kV",
            length=haversine_length
        )
