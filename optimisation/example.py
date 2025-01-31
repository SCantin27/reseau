import pypsa

# Path to the folder containing your CSV files
input_folder_path = r"C:\Users\TABLET\Documents\GitHub\reseau\optimisation\input"
output_folder_path = r"C:\Users\TABLET\Documents\GitHub\reseau\optimisation\output"

# Initialize a PyPSA network and import the CSV data
n = pypsa.Network()
n.import_from_csv_folder(input_folder_path)

# run the optimisation
n.optimize()    

csv_folder_path = r"C:\Users\TABLET\Documents\GitHub\reseau\optimisation\csv"

n.export_to_csv_folder(output_folder_path)

# plot results
n.generators_t.p.plot()
n.plot()

# get statistics
n.statistics()
n.statistics.energy_balance()

print(n.generators_t.p)