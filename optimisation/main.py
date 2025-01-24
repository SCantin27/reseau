import pypsa

# load an example network
n = pypsa.Network.import_from_netcdf('.ac-dc-meshed/ac-dc-data.nc')

# run the optimisation
n.optimize()

# plot results
n.generators_t.p.plot()
n.plot()

# get statistics
n.statistics()
n.statistics.energy_balance()