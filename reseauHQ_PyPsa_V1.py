import pypsa
import numpy as np
import matplotlib.pyplot as plt

from Composants.Buses import add_buses_to_network
from Composants.Lines import ajouter_lignes


#Create network
network = pypsa.Network()

#Add buses, generators and laods
add_buses_to_network(network)


# network.add("Bus", name="Montreal", x=-73.5673, y=45.5017,v_nom=735,control="PQ")

# network.add("Load", name="Consommation de montreal", p_set=2000, q_set=100,control="PQ")

#Add lines
ajouter_lignes(network)
pypsa.pf.apply_line_types(network)


print(network.loads)
print(network.lines)
print(network.buses)
print(network.buses['control'])



# Perform power flow calculation
network.pf()

# Extract and print power flow results
print("Power flow on lines (p0):")
print(network.lines_t.p0)

print("\nVoltage angles (degrees):")
print(network.buses_t.v_ang * 180 / np.pi)

print("\nVoltage magnitudes (p.u.):")
print(network.buses_t.v_mag_pu)
""" 
#Plotting parameters
fig, ax = plt.subplots(figsize=(15, 8))
network.plot(
    color_geomap={'ocean': 'lightblue','land': 'lightgreen'},
    bus_sizes=0.01,
    line_colors='black',
    line_alpha=1,
    line_widths=0.001,
    flow = network.snapshots[0],
    title="HQ Power Network Visualization Proof of concept",
)

# Show the plot
plt.show()


 """