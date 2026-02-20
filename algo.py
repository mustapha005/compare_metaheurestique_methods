import random
import math
import numpy as np
import tsplib95


# ─── TSP Loader ───────────────────────────────────────────────────────────────

def load_tsp_to_matrix(filename):
    problem = tsplib95.load(filename)
    available_nodes = sorted(problem.node_coords.keys())
    coords = {node_id: tuple(problem.node_coords[node_id]) for node_id in available_nodes}
    node_list = sorted(coords.keys())
    n = len(node_list)
    distance_matrix = np.zeros((n, n))
    for i, node_i in enumerate(node_list):
        for j, node_j in enumerate(node_list):
            if i != j:
                coord_i = np.array(coords[node_i])
                coord_j = np.array(coords[node_j])
                distance_matrix[i, j] = np.linalg.norm(coord_i - coord_j)
    return distance_matrix


def get_total_distance(distance_matrix, solution):
    return sum(
        distance_matrix[solution[i], solution[(i + 1) % len(solution)]]
        for i in range(len(solution))
    )


def random_solution(n):
    sol = list(range(n))
    random.shuffle(sol)
    return sol


# ─── Neighborhoods ────────────────────────────────────────────────────────────

def swap(solution):
    new = solution.copy()
    i, j = random.sample(range(len(solution)), 2)
    new[i], new[j] = new[j], new[i]
    return new


def two_opt(solution):
    new = solution.copy()
    i, j = sorted(random.sample(range(len(solution)), 2))
    new[i:j] = new[i:j][::-1]
    return new



# ─── Tabu Search ──────────────────────────────────────────────────────────────

def tabu_search(distance_matrix, neighborhood, max_iter=1000, tabu_size=10):
    n = len(distance_matrix)
    current = random_solution(n)
    current_cost = get_total_distance(distance_matrix, current)
    best_solution, best_cost = current.copy(), current_cost
    tabu_list = []
    tested = explored = 0

    for _ in range(max_iter):
        neighbors = [neighborhood(current) for _ in range(20)]
        best_neighbor, best_neighbor_cost = None, float('inf')

        for neighbor in neighbors:
            tested += 1
            neighbor_cost = get_total_distance(distance_matrix, neighbor)
            if neighbor_cost < best_neighbor_cost and neighbor not in tabu_list:
                best_neighbor, best_neighbor_cost = neighbor, neighbor_cost

        if best_neighbor is not None:
            current, current_cost = best_neighbor, best_neighbor_cost
            explored += 1
            tabu_list.append(best_neighbor)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)
            if current_cost < best_cost:
                best_solution, best_cost = current.copy(), current_cost

    return best_solution, best_cost, tested, explored