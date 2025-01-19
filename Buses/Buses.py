def add_buses_to_network(network):
    
    centrales = [
        ("La-Grande-2", -77.7056, 53.7767),
        # ("La-Grande-1", -77.6869, 53.7822),
        # ("La-Grande-3", -77.6419, 53.7578),
        # ("La-Grande-4", -77.6083, 53.7461),
        # ("La-Grande-5", -77.5672, 53.7281),
        # ("Caniapiscau", -72.9569, 51.4956),
        # ("Eastmain-1", -77.0972, 52.2133),
        # ("Eastmain-1-A", -77.0811, 52.2447),
        # ("Robert-Bourassa", -78.4406, 53.7800),
        # ("René-Lévesque", -77.9736, 53.6400),
        # ("Manic-5", -68.7250, 50.6000),
        # ("Centrale de Chute-aux-Outardes", -68.4928, 50.5300),
        # ("Centrale de la Romaine", -64.6269, 50.1156),
        # ("Gérard-D.-L.-Levesque", -77.2186, 52.3600),
        # ("Jean-Lesage", -70.5794, 51.9292),
        # ("Mitis", -68.1050, 48.6883),
        # ("Beauharnois", -73.7342, 45.2569),
        # ("Des Cèdres", -73.5536, 45.2217),
        # ("Saint-Laurent", -72.9742, 45.0750),
        # ("Îles-de-la-Madeleine", -61.7967, 47.3686),
        # ("Lac-Saint-Jean", -71.3258, 48.5650),
        # ("Péribonka", -71.3464, 48.6364),
        # ("Barrage de la Grande-2", -77.7056, 53.7767),
        # ("Barrage de la Grande-3", -77.6419, 53.7578),
        # ("Barrage de la Grande-4", -77.6083, 53.7461),
        # ("Barrage de la Grande-5", -77.5672, 53.7281),
        # ("Barrage du Caniapiscau", -72.9569, 51.4956),
        # ("Barrage de la Romaine", -64.6269, 50.1156),
        # ("Centrale de Manic-2", -68.7256, 50.6494),
        # ("Centrale de Manic-1", -68.7397, 50.4681),
        # ("Barrage de Chute-aux-Outardes", -68.4928, 50.5300),
        # ("Barrage de Rivière-aux-Rats", -70.5553, 48.9931)
    ]

    for name, lon, lat in centrales:
        network.add("Bus", name=name, x=lon, y=lat)

    postes = [
        # ("Manic-5", -68.9390, 50.2940),
        # ("Micoua", -68.6400, 50.2370),
        # ("Radisson", -77.7460, 53.7490),
        # ("Chenier", -73.4010, 45.3690),
        # ("Haute-Cote-Nord", -69.7250, 49.0420),
        # ("Metapelutin", -74.6640, 49.5160),
        # ("Outaouais", -75.4950, 45.3820),
        # ("Cote-Nord", -68.7000, 50.2000),
        # ("Baie-James", -77.8000, 49.4200),
        # ("Mauricie", -72.5480, 46.3440),
        # ("Montérégie", -73.4510, 45.2990),
        # ("Capitale-Nationale", -71.2140, 46.7710),
        # ("Gaspesie", -64.2070, 48.5620),
        # ("Abitibi-Temiscamingue", -78.3450, 48.5090)
    ]

    for name, lon, lat in postes:
        network.add("Bus", name=name, x=lon, y=lat)

    villes = [
        ("Montreal", -73.5673, 45.5017),
        # ("Quebec", -71.2082, 46.8139),
        # ("Laval", -73.7402, 45.5774),
        # ("Gatineau", -75.7110, 45.4767),
        # ("Sherbrooke", -71.8993, 45.4000),
        # ("Trois-Rivieres", -72.5480, 46.3440),
        # ("Drummondville", -72.4632, 45.8762),
        # ("Saguenay", -71.2082, 48.4291),
        # ("Longueuil", -73.5023, 45.5017),
        # ("Chicoutimi", -71.2090, 48.4284),
        # ("Terrebonne", -73.6989, 45.7747),
        # ("Repentigny", -73.6955, 45.7394),
        # ("Rouyn-Noranda", -79.0310, 48.2382),
        # ("Victoriaville", -71.9877, 46.0583),
        # ("Baie-Comeau", -68.1530, 49.2183),
        # ("Sept-Iles", -66.3680, 50.2080),
        # ("Rimouski", -68.5191, 48.4484),
        # ("Bromont", -72.6533, 45.3008),
        # ("Carleton-sur-Mer", -66.1533, 48.1003)
    ]

    for name, lon, lat in villes:
        network.add("Bus", name=name, x=lon, y=lat)