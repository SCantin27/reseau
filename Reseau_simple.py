import pypsa
import matplotlib.pyplot as plt

# Create network
n = pypsa.Network()

# Add buses with carriers

# Slack Node : Artificial node that take the power imbalance - Do not remove
n.add("Bus", name="SlackBus", v_nom=735)

n.add("Bus", name="GenBus1", v_nom=735)
n.add("Bus", name="GenBus2", v_nom=735)
n.add("Bus", name="GenBus3", v_nom=735)
n.add("Bus", name="GenBus4", v_nom=735)
n.add("Bus", name="GenBus5", v_nom=735)

n.add("Bus", name="LoadBus1", v_nom=735)
n.add("Bus", name="LoadBus2", v_nom=735)
n.add("Bus", name="LoadBus3", v_nom=735)
n.add("Bus", name="LoadBus4", v_nom=735)
n.add("Bus", name="LoadBus5", v_nom=735)

n.add("Bus", name="NeutralBus1", v_nom=735)
n.add("Bus", name="NeutralBus2", v_nom=735)

# Add Slack Bus Generator
n.add("Generator", name="SlackGen", bus="SlackBus", p_nom=1000, control="Slack", marginal_cost=1000)
n.generators.loc["SlackGen", "p_nom_extendable"] = True  # Allow extension of p_nom if needed

# Add other generators
n.add("Generator", name="Gen1", bus="GenBus1", p_nom=1000, q_min=-10, q_max=10, control="PV", marginal_cost=1)
n.add("Generator", name="Gen2", bus="GenBus2", p_nom=2000, q_min=-20, q_max=20, control="PV", marginal_cost=2)
n.add("Generator", name="Gen3", bus="GenBus3", p_nom=3000, q_min=-30, q_max=30, control="PV", marginal_cost=3)
n.add("Generator", name="Gen4", bus="GenBus4", p_nom=4000, q_min=-40, q_max=40, control="PV", marginal_cost=4)
n.add("Generator", name="Gen5", bus="GenBus5", p_nom=5000, q_min=-50, q_max=50, control="PV", marginal_cost=5)

# Add Load
n.add("Load", name="Load1", bus="LoadBus1", control="PQ", p_set=500)
n.add("Load", name="Load2", bus="LoadBus2", control="PQ", p_set=1000)
n.add("Load", name="Load3", bus="LoadBus3", control="PQ", p_set=1500)
n.add("Load", name="Load4", bus="LoadBus4", control="PQ", p_set=2000)
n.add("Load", name="Load5", bus="LoadBus5", control="PQ", p_set=2500)

# Add Transmission Lines
n.add("Line", name="Gen1-Gen2", bus0="GenBus1", bus1="GenBus2", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Gen2-Gen3", bus0="GenBus2", bus1="GenBus3", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Gen3-Neutral1", bus0="GenBus3", bus1="NeutralBus1", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Gen4-Neutral1", bus0="GenBus4", bus1="NeutralBus1", x=10, r=1, g=0.00049, s_nom=100000)

n.add("Line", name="Neutral1-Neutral2", bus0="NeutralBus1", bus1="NeutralBus2", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Neutral1-Neutral2(2)", bus0="NeutralBus1", bus1="NeutralBus2", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Neutral1-Neutral2(3)", bus0="NeutralBus1", bus1="NeutralBus2", x=10, r=1, g=0.00049, s_nom=100000)

n.add("Line", name="Gen5-Load5", bus0="GenBus5", bus1="LoadBus5", x=10, r=1, g=0.00049, s_nom=100000)

n.add("Line", name="Neutral2-Load5", bus0="NeutralBus2", bus1="LoadBus5", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Neutral2-Load4", bus0="NeutralBus2", bus1="LoadBus4", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Neutral2-Load3", bus0="NeutralBus2", bus1="LoadBus3", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Neutral2-Load3(2)", bus0="NeutralBus2", bus1="LoadBus3", x=10, r=1, g=0.00049, s_nom=100000)

n.add("Line", name="Load3-Load2", bus0="LoadBus3", bus1="LoadBus2", x=10, r=1, g=0.00049, s_nom=100000)
n.add("Line", name="Load2-Load1", bus0="LoadBus2", bus1="LoadBus1", x=10, r=1, g=0.00049, s_nom=100000)


n.add("Line", name="Slack-Neutral1", bus0="SlackBus", bus1="NeutralBus1", x=1e-6, r=1e-7, s_nom=100000)

# Optimize the network : Run the DC PowerFlow to evaluate optimal generation dispatch
n.optimize()

# Set the generation of each generators to it's optimal value for the AC powerflow
n.generators.loc["Gen1", "p_set"] = p_opt_gen1 = n.generators_t.p["Gen1"].iloc[-1]
n.generators.loc["Gen2", "p_set"] = p_opt_gen2 = n.generators_t.p["Gen2"].iloc[-1]
n.generators.loc["Gen3", "p_set"] = p_opt_gen3 = n.generators_t.p["Gen3"].iloc[-1]
n.generators.loc["Gen4", "p_set"] = p_opt_gen4 = n.generators_t.p["Gen4"].iloc[-1]
n.generators.loc["Gen5", "p_set"] = p_opt_gen5 = n.generators_t.p["Gen5"].iloc[-1]

# Calculate the total load amount and estimate the line losses
total_load = n.loads_t.p.sum().sum()
line_loss_initial_estimation = total_load * 0.1

# List the number of generators not operating at their maximum output
generators_not_at_max = [gen for gen in n.generators.index if n.generators.loc[gen, "p_set"] < n.generators.loc[gen, "p_nom"]]

# Sort generators by marginal cost
sorted_generators = n.generators.loc[generators_not_at_max].sort_values(by="marginal_cost").index

# Dispatch the line loss estimation to each generator not operating at its maximum output
remaining_loss = line_loss_initial_estimation
for gen in sorted_generators:
    if remaining_loss <= 0:
        break
    available_capacity = n.generators.loc[gen, "p_nom"] - n.generators.loc[gen, "p_set"]
    if available_capacity >= remaining_loss:
        n.generators.loc[gen, "p_set"] += remaining_loss
        remaining_loss = 0
    else:
        n.generators.loc[gen, "p_set"] += available_capacity
        remaining_loss -= available_capacity

# Run the AC PowerFlow
n.pf()

# Check the power generated by the Slack generator
slack_power = n.generators_t.p["SlackGen"].iloc[-1]

# While the power generated by the Slack generator is greater than 0.1% of the total load, distribute the slack generator's power to generators not at their maximum output
iterations = 0
while slack_power > total_load / 1000:
    # Distribute the Slack generator's power to generators not at their maximum output
    remaining_slack_power = slack_power
    for gen in sorted_generators:
        if remaining_slack_power <= 0:
            break
        available_capacity = n.generators.loc[gen, "p_nom"] - n.generators.loc[gen, "p_set"]
        if available_capacity >= remaining_slack_power:
            n.generators.loc[gen, "p_set"] += remaining_slack_power
            remaining_slack_power = 0
        else:
            n.generators.loc[gen, "p_set"] += available_capacity
            remaining_slack_power -= available_capacity

    # Run the AC PowerFlow again with updated values of p_set
    n.pf()

    # Check the power generated by the Slack generator
    slack_power = n.generators_t.p["SlackGen"].iloc[-1]

    iterations += 1


print("------------------------------------------------------------------------------------------")

# Display results

print("Number of iterations: ", iterations)

print("\nPower generated by each generator (p):")
print(n.generators_t.p)

print("\nPower received by the load (p):")
print(n.loads_t.p)

print("\nPower losses on each lines :")
print(abs(n.lines_t.p0 + n.lines_t.p1))

print("------------------------------------------------------------------------------------------")
#Powerflow on each line
print("\nPowerflow on each line :")
print(n.lines_t.p0)

print("------------------------------------------------------------------------------------------")

print("\nTotal Gen :")
print(round(n.generators_t.p.sum().sum(),0))

print("\nTotal Load :")
print(n.loads_t.p.sum().sum())

print("\nTotal Losses :")
print(round(n.generators_t.p.sum().sum() - n.loads_t.p.sum().sum(),0))
