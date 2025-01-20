import pypsa
import numpy as np
import matplotlib.pyplot as plt

from Composants.Buses import add_buses_to_network
from Composants.Lines import ajouter_lignes


#Create network
network = pypsa.Network()

#Add buses, generators and laods
add_buses_to_network(network)

#Add lines
ajouter_lignes(network)


print(network.loads)
print(network.lines)

# Perform power flow calculation
network.pf()

# Extract and print power flow results
print("Power flow on lines (p0):")
print(network.lines_t.p0)

print("\nVoltage angles (degrees):")
print(network.buses_t.v_ang * 180 / np.pi)

print("\nVoltage magnitudes (p.u.):")
print(network.buses_t.v_mag_pu)

# #Plotting parameters
# fig, ax = plt.subplots(figsize=(15, 8))
# network.plot(
#     color_geomap={'ocean': 'lightblue','land': 'lightgreen'},
#     bus_sizes=0.01,
#     line_colors='black',
#     line_alpha=1,
#     line_widths=0.001,
#     flow = network.snapshots[0],
#     title="HQ Power Network Visualization Proof of concept",
# )

# # Show the plot
# plt.show()


