import pypsa
import numpy as np
import matplotlib.pyplot as plt

from Buses.Buses import add_buses_to_network


network = pypsa.Network()

add_buses_to_network(network)

print(network.buses)
print(network.generators)


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
