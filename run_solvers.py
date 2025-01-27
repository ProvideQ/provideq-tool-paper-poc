import csv
import math
import os
from toolbox_python_api.api import ProvideQApi

def get_problems_in_dir(directory, extension):
    # List to store file contents
    content_list = []
    
    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        # Filter out .vrp files
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        # Read the content of the file and append it to the list
                        content_list.append((file, f.read()))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return content_list

def get_all_vrp_problems():
    return get_problems_in_dir(f'./problems/vrp', '.vrp')

def get_all_knapsack_problems():
    return get_problems_in_dir(f'./problems/knapsack', '.txt')

def get_dimension(vrp):
    for line in vrp.splitlines():
        # if line starts with DIMENSION
        if line.startswith("DIMENSION"):
            # return the number after the colon
            return int(line.split(":")[1].strip())

    raise Exception("No Dimension found in vrp: " + vrp)

def get_max_cluster_amount(vrp):
    dimension = get_dimension(vrp)
    max_cluster_size = 8 # determined by quantum solver
    return math.ceil(dimension / max_cluster_size)

def get_kmeans_settings(vrp):
    return {
        "edu.kit.provideq.toolbox.vrp.clusterer.KmeansClusterer": lambda: [
            {
                "name": "Cluster Number",
                "type": "INTEGER",
                "required": False,
                "description": "",
                "min": 1,
                "max": 1000,
                "value": get_max_cluster_amount(vrp),
            }
        ],
    }

def get_vrp_solution_quality(vrp_solution):
    # Example first line
    # NAME : small sample solved with length 18.465723173284992
    # Extract decimal number at end of first line
    first_line = vrp_solution.splitlines()[0]
    return float(first_line.split()[-1])

def get_knapsack_solution_quality(knapsack_solution):
    # First line has number with total value of items
    return int(knapsack_solution.splitlines()[0])

def test(problem_type, get_problems, solver, solver_name, solver_per_type, create_settings_for_problem, get_solution_quality):
    for (name, problem) in get_problems():
        print(f"Solving {name} with {solver_name}...")
        solution = api.solve(problem_type, problem, solver, solver_per_type, create_settings_for_problem(problem))
        solution_quality = get_solution_quality(solution['solutionData'])

        writer.writerow([name, solver_name, solution['executionMilliseconds'], solution_quality])
        print(f"Solved {name} with {solver_name} in {solution['executionMilliseconds']}ms with quality {solution_quality}")

def test_vrp_with_kmeans_and_lkh():
    solver_per_type = {
        "vrp": lambda: "edu.kit.provideq.toolbox.vrp.solvers.LkhVrpSolver",
        "cluster-vrp": lambda: "edu.kit.provideq.toolbox.vrp.clusterer.KmeansClusterer",
    }

    test(
        "vrp", get_all_vrp_problems,
        "edu.kit.provideq.toolbox.vrp.solvers.ClusterAndSolveVrpSolver", "LkhVrpSolver with KmeansClusterer",
        solver_per_type, get_kmeans_settings, get_vrp_solution_quality)

def test_vrp_with_kmeans_and_xxxxxxxxxxxxxx():
    solver_per_type = {
        "vrp": lambda: "edu.kit.provideq.toolbox.vrp.solvers.xxxxxxxxxxxxxx",
        "cluster-vrp": lambda: "edu.kit.provideq.toolbox.vrp.clusterer.KmeansClusterer",
    }

    test(
        "vrp", get_all_vrp_problems,
        "edu.kit.provideq.toolbox.vrp.solvers.ClusterAndSolveVrpSolver", "xxxxxxxxxxxxxx with KmeansClusterer",
        solver_per_type, get_kmeans_settings, get_vrp_solution_quality)

def test_knapsack_with_hs():
    test(
        "knapsack", get_all_knapsack_problems,
        "edu.kit.provideq.toolbox.knapsack.solvers.PythonKnapsackSolver", "Horowitz-Sahni Knapsack",
        {}, lambda _: {}, get_knapsack_solution_quality)

def test_knapsack_with_qiskit():
    test(
        "knapsack", get_all_knapsack_problems,
        "edu.kit.provideq.toolbox.knapsack.solvers.QiskitKnapsackSolver", "Qiskit Knapsack",
        {}, lambda _: {}, get_knapsack_solution_quality)


# Choose local or server
# base_url = "https://api.provideq.kit.edu"
base_url = "https://betaapi.provideq.kit.edu"
# base_url = "http://localhost:8080"

api = ProvideQApi(base_url)

with open('results.csv', mode='a', newline='') as file:
    writer = csv.writer(file)

    # Write the header if the file is empty
    if file.tell() == 0:
        writer.writerow(['problem', 'solver', 'time_milliseconds', 'solution_quality'])

    test_vrp_with_kmeans_and_lkh()
    # test_vrp_with_kmeans_and_xxxxxxxxxxxxxx()

    test_knapsack_with_hs()
    test_knapsack_with_qiskit()
