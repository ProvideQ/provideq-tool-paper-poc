import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("results_vrp.csv")

# Sort the data by Solvername and Problemname
df.sort_values(by=["Solvername", "Problemname"], inplace=True)

# Extract unique problem names
problems = df["Problemname"].unique()
solvers = df["Solvername"].unique()

# Plotting
plt.figure(figsize=(6, 3))

for solver in solvers:
    solver_df = df[df["Solvername"] == solver]
    # special print for optimal solutions
    if (solver == "Optimal Solution (with Clustering)"):
        plt.plot(solver_df["Problemname"], solver_df["Solution (Kilometer)"], marker='.', linestyle='--', color='grey', label=solver)
    elif (solver == "Optimal Solution (without Clustering)"):
        plt.plot(solver_df["Problemname"], solver_df["Solution (Kilometer)"], marker='.', linestyle='--', color='green', label=solver)
    elif (solver == "2-Phase with D-Wave"):
        plt.scatter(solver_df["Problemname"], solver_df["Solution (Kilometer)"], marker='D', color='blue', s=70, label=solver)
    else:
       plt.plot(solver_df["Problemname"], solver_df["Solution (Kilometer)"], marker='o', color = 'black', label=solver)

plt.xlabel("Problem Name")
plt.ylabel("Solution (Kilometer)")
plt.title("Solutions by Problem and Solver")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.grid()
plt.show()