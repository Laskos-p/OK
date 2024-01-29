import math
from time import time
from copy import deepcopy
from utils import visualize_schedule, tabu_neighbor


def greedy(processors: int, tasks: list, pre_sort: bool = False) -> tuple:
    """
    Greedy algorithm
    :param processors: number of processors
    :param tasks: list of tasks
    :param pre_sort: sort tasks before scheduling

    :return: longest processor time, time of scheduling, list of processors with tasks
    """
    if pre_sort:
        tasks.sort(reverse=True)

    proc_list = [[0, []] for _ in range(processors)]
    start = time()
    while tasks:
        proc_list.sort(key=lambda x: x[0])
        proc_list[0][1].append(tasks[0])
        proc_list[0][0] += tasks[0]
        tasks.pop(0)

    execution_time = time() - start
    processor_time = max(proc_list, key=lambda x: x[0])[0]
    return processor_time, execution_time, proc_list


def objective_function(proc_list):
    """
    Function to evaluate quality of solution
    :param proc_list: list of processors with tasks

    :return: longest processor time, number of processors with the longest processor length,
        negative value of difference between longest and shortest processor, lowest task in the longest processor
    """
    # evaluate quality of solution
    proc_list.sort(key=lambda x: x[0])

    longest_processor = max(proc_list)[0]
    longest_processors = len([processor for processor in proc_list if processor[0] == longest_processor])
    difference = longest_processor - proc_list[0][0]
    lowest_task = min([min(process[1]) for process in proc_list if process[0] == longest_processor])
    return longest_processor, longest_processors, -difference, lowest_task


def get_neighbors(solution, i):
    """
    Get neighbors of solution
    :param solution: list of processors with tasks
    :param i: index of task to move or swap

    :return: time spent to find neighbors, list of neighbors
    """
    start = time()
    neighbors = []
    solution.sort(key=lambda x: x[0], reverse=True)

    for j, [_, other_processor_tasks] in enumerate(solution[:0:-1], start=1):

        # move task to other processor
        neighbor = deepcopy(solution)
        task = neighbor[0][1].pop(i)
        neighbor[-j][1].append(task)

        # neighbor[0][1].sort(reverse=True)
        neighbor[-j][1].sort(reverse=True)

        neighbor[0][0] -= task
        neighbor[-j][0] += task

        neighbors.append(neighbor)

        for k, other_processor_task in enumerate(other_processor_tasks):

            # swap tasks
            neighbor = deepcopy(solution)
            difference = neighbor[0][1][i] - neighbor[-j][1][k]
            neighbor[0][1][i], neighbor[-j][1][k] = neighbor[-j][1][k], neighbor[0][1][i]

            neighbor[0][1].sort(reverse=True)
            neighbor[-j][1].sort(reverse=True)

            neighbor[0][0] -= difference
            neighbor[-j][0] += difference

            neighbors.append(neighbor)

    return time() - start, neighbors


def tabu_search(processors: int, tasks: list, max_iterations: int, tabu_list_size: int, time_limit: int = 60 * 5,
                draw: bool = False):
    """
    Tabu search algorithm
    :param processors: number of processors
    :param tasks: list of tasks
    :param max_iterations: number of iterations
    :param tabu_list_size: length of tabu list
    :param time_limit: time limit in seconds
    :param draw: draw plots

    :return: best solution, time of scheduling, time of finding all neighbors, time of tabu algorithm
    """
    # calculate optimum
    optimum = int(math.ceil(sum(tasks) / processors))

    # generate initial solution using greedy algorith with reverse sorting of tasks
    greedy_scheduling_time, initial_solution = greedy(processors, tasks, pre_sort=True)[1:]

    print("Initial solution:")
    print(*initial_solution, sep="\n")

    best_solution = initial_solution
    current_solution = initial_solution
    tabu_list = []
    full_neighbour_finding_time = 0
    step_instances = []

    if draw:
        step_instances.append(initial_solution)
        visualize_schedule(current_solution)
        print("generated plot")

    print("Optimum: ", optimum)

    start = time()
    for iteration in range(max_iterations):
        if draw:
            visualize_schedule(current_solution)
            print("generated plot")

        fitness_best_solution = objective_function(best_solution)
        best_neighbor = None
        best_neighbor_fitness = (float('inf'), float('inf'), float('inf'), float('inf'))
        current_solution.sort(key=lambda x: x[0], reverse=True)

        # for each task in the longest processor
        for i in range(len(current_solution[0][1])):

            # get neighbors of current solution with task on index i moved or swapped
            neighbor_finding_time, neighbors = get_neighbors(current_solution, i)
            full_neighbour_finding_time += neighbor_finding_time

            # for each neighbor
            for neighbor in neighbors:

                # if neighbor is not in tabu list
                if not tabu_neighbor(neighbor, tabu_list):
                    neighbor_fitness = objective_function(neighbor)

                    # if neighbor is better than current best neighbor update best neighbor
                    if neighbor_fitness < best_neighbor_fitness:
                        best_neighbor = neighbor
                        best_neighbor_fitness = neighbor_fitness

                    # if neighbor is better than current best solution
                    # update the best solution and skip the checking of other neighbors
                    if neighbor_fitness[0] < fitness_best_solution[0] or \
                            neighbor_fitness[0] == fitness_best_solution[0] and \
                            neighbor_fitness[1] < fitness_best_solution[1]:
                        print("Skipped")
                        break
            else:
                continue
            break

        if best_neighbor is None:
            # No non-tabu neighbors found,
            # terminate the search
            print("No non-tabu neighbors found")
            break

        current_solution = best_neighbor
        tabu_list.append(sorted(best_neighbor))

        if len(tabu_list) > tabu_list_size:
            # Remove the oldest entry from the
            # tabu list if it exceeds the size
            tabu_list.pop(0)

        print("Current best neighbor: ", objective_function(best_neighbor),
              "Current best solution: ", objective_function(best_solution))
        print("Current iteration: ", iteration)

        if objective_function(best_neighbor) < objective_function(best_solution):
            # Update the best solution if the current neighbor is better
            print("Found better solution: ", objective_function(best_neighbor))
            best_solution = best_neighbor

        if time() - start > time_limit:
            print("Time limit reached, time: ", time() - start, "s")
            break

        if objective_function(best_solution)[0] == optimum:
            print("Found optimum: ", objective_function(best_solution)[0], "in iteration: ", iteration)
            break

    tabu_algorithm_time = time() - start

    return best_solution, greedy_scheduling_time, full_neighbour_finding_time, tabu_algorithm_time
