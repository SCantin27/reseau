import pypsa
import numpy as np
import matplotlib.pyplot as plt

from Buses.Buses import add_buses_to_network


network = pypsa.Network()

add_buses_to_network(network)

print(network.buses)


# Add lines between buses

network.add("Line", "Ligne1",
                bus0="La-Grande-2",
                bus1="Montreal",
                x=0.33,
                r=0.01)

print(network.lines)

# network.add("Line", "Ligne2",
#                 bus0="Manic-5",
#                 bus1="Quebec",
#                 x=0.33,
#                 r=0.01)

# network.add("Line", "Ligne3",
#                 bus0="Montreal",
#                 bus1="Quebec",
#                 x=0.33,
#                 r=0.01)

# network.add("Line", "Ligne4",
#                 bus0="Gaspesie",
#                 bus1="Sherbrooke",
#                 x=0.33,
#                 r=0.01)         

# network.add("Line", "Ligne5",
#                 bus0="La Verendrye",
#                 bus1="Quebec",
#                 x=0.33,
#                 r=0.01)    

# network.add("Line", "Ligne du Nord",
#                 bus0="Manic",
#                 bus1="Quebec",
#                 x=0.33,
#                 r=0.01)

# network.add("Line", "Ligne Baie James",
#                 bus0="Micoua",
#                 bus1="Saguenay",
#                 x=0.33,
#                 r=0.01)

# Add generators

network.add("Generator", "La-Grande-2",
            bus="La-Grande-2",
            p_set=3000,
            control="PQ")

# network.add("Generator", "Manic",
#             bus="Manic",
#             p_set=2660,
#             control="PQ")

# network.add("Generator", "LG2",
#             bus="Baie James",
#             p_set=5616,
#             control="PQ")

# network.add("Generator", "Carleton",
#             bus="Carleton",
#             p_set=68,
#             control="PQ")

print(network.generators)

# Add loads
network.add("Load", "Montreal",
            bus="Montreal",
            p_set=2000,
            q_set=100)

# network.add("Load", "Qc consomption",
#             bus="Quebec",
#             p_set=4000,
#             q_set=80)
print(network.loads)

# Perform power flow calculation
network.pf()

#Plot the network with the desired formatting
fig, ax = plt.subplots(figsize=(15, 8))
network.plot(
    color_geomap={'ocean': 'lightblue','land': 'lightgreen'},
    bus_sizes=0.01,
    line_colors='black',
    line_alpha=1,
    line_widths=0.002,
    flow = network.snapshots[0],
    title="HQ Power Network Visualization Proof of concept",
)


# # Show the plot
plt.show()

# # Extract and print power flow results
# print("Power flow on lines (p0):")
# print(network.lines_t.p0)

# print("\nVoltage angles (degrees):")
# print(network.buses_t.v_ang * 180 / np.pi)

# print("\nVoltage magnitudes (p.u.):")
# print(network.buses_t.v_mag_pu)
