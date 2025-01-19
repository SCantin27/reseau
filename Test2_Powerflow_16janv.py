import pypsa
import numpy as np
import matplotlib.pyplot as plt

network = pypsa.Network()

#Test Commit

# Add buses
network.add("Bus", "Manic", v_nom=735, x=-68.7346799, y=50.6398823)
network.add("Bus", "Baie James", v_nom=735, x=-77.5860832, y=53.781295)
network.add("Bus", "Montreal", v_nom=735, x=-73.609156, y=45.5072858)
network.add("Bus", "Beauharnois", v_nom=735, x=-73.9135513, y=45.3129227)
network.add("Bus", "Carleton", v_nom=735, x=-66.6173117, y=48.1367404)
network.add("Bus", "Quebec", v_nom=735, x=-71.2773173, y=46.7817463)
network.add("Bus", "La Verendrye", v_nom=735, x=-74.9361229, y=47.496299)


# Add lines between buses

network.add("Line", "Ligne1",
                bus0="Beauharnois",
                bus1="Montreal",
                x=0.33,
                r=0.01)

network.add("Line", "Ligne2",
                bus0="Carleton",
                bus1="Quebec",
                x=0.33,
                r=0.01)

network.add("Line", "Ligne3",
                bus0="Montreal",
                bus1="Quebec",
                x=0.33,
                r=0.01)

network.add("Line", "Ligne4",
                bus0="La Verendrye",
                bus1="Montreal",
                x=0.33,
                r=0.01)         

network.add("Line", "Ligne5",
                bus0="La Verendrye",
                bus1="Quebec",
                x=0.33,
                r=0.01)    

network.add("Line", "Ligne du Nord",
                bus0="Manic",
                bus1="Quebec",
                x=0.33,
                r=0.01)

network.add("Line", "Ligne Baie James",
                bus0="Baie James",
                bus1="La Verendrye",
                x=0.33,
                r=0.01)

# Add generators

network.add("Generator", "Beauharnois",
            bus="Beauharnois",
            p_set=1903,
            control="PQ")

network.add("Generator", "Manic",
            bus="Manic",
            p_set=2660,
            control="PQ")

network.add("Generator", "LG2",
            bus="Baie James",
            p_set=5616,
            control="PQ")

network.add("Generator", "Carleton",
            bus="Carleton",
            p_set=68,
            control="PQ")

# Add loads
network.add("Load", "Mtl consomption",
            bus="Montreal",
            p_set=6000,
            q_set=100)

network.add("Load", "Qc consomption",
            bus="Quebec",
            p_set=4000,
            q_set=80)

# Perform power flow calculation
network.pf()

# Plot the network with the desired formatting
fig, ax = plt.subplots(figsize=(15, 8))
network.plot(
    color_geomap={'ocean': 'lightblue','land': 'lightgreen'},
    bus_colors={'Baie James': 'red','Quebec':'blue', 'Carleton':'red', 'Beauharnois':'red', 'Manic': 'red','Montreal': 'blue', 'La Verendrye':'red'},
    bus_sizes=0.01,
    line_colors='black',
    line_alpha=1,
    line_widths=0.002,
    flow = network.snapshots[0],
    title="HQ Power Network Visualization Proof of concept",
)


# Show the plot
plt.show()

# Extract and print power flow results
print("Power flow on lines (p0):")
print(network.lines_t.p0)

print("\nVoltage angles (degrees):")
print(network.buses_t.v_ang * 180 / np.pi)

print("\nVoltage magnitudes (p.u.):")
print(network.buses_t.v_mag_pu)
