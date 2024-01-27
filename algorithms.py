import math
from time import time, time_ns
from copy import deepcopy

import algorithms
# from collections import defaultdict
from utils import visualize_schedule, instances_are_equal
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count


def greedy(processors: int, tasks: list, pre_sort: bool = False) -> tuple:
    """
    Algorytm zachlanny
    :param processors: liczba procesorow
    :param tasks: lista procesow
    :param pre_sort: wstępne sortowanie

    :return: (dlugosc wykonywania procesow, czas wykonania, lista 2d z procesami na procesorach)
    """
    if pre_sort:
        tasks.sort(reverse=True)

    # proc = [0 for _ in range(processors)]
    proc_list = [[0, []] for _ in range(processors)]  # [suma_czasu, [czas_procesu1, czas_procesu2, ...]]
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
    # evaluate quality of solution
    proc_list.sort(key=lambda x: x[0])
    longest_processor = max(proc_list)[0]
    longest_processors = len([processor for processor in proc_list if processor[0] == longest_processor])
    difference = longest_processor - proc_list[0][0]
    lowest_task = min(proc_list[-1][1])
    # return max(proc_list, key=lambda x: x[0])[0]
    # optimal_length_processors = len([processor for processor in proc_list if processor[0] == 3458])
    # return longest_processor, longest_processors, -difference, -optimal_length_processors

    return longest_processor, longest_processors, -difference, lowest_task


# def get_neighbor(i, solution):
#     neighbors = []
#     for j, [processor_length, other_processor_tasks] in enumerate(solution[1:], start=1):
#         # if processor have the same length as longest processor go to next processor
#         # for every task in that processor check if it's shorter than the longest processor task
#         neighbor = deepcopy(solution)
#         task = neighbor[0][1].pop(i)
#         neighbor[j][1].append(task)
#         # neighbor[0][1].sort(reverse=True)
#         neighbor[j][1].sort(reverse=True)
#         #     # update processor length
#         neighbor[0][0] -= task
#         neighbor[j][0] += task
#
#         neighbors.append(neighbor)
#         for k, other_processor_task in enumerate(other_processor_tasks):
#             neighbor = deepcopy(solution)
#             difference = neighbor[0][1][i] - neighbor[j][1][k]
#             neighbor[0][1][i], neighbor[j][1][k] = neighbor[j][1][k], neighbor[0][1][i]
#
#             neighbor[0][1].sort(reverse=True)
#             neighbor[j][1].sort(reverse=True)
#             # update processor length
#             neighbor[0][0] -= difference
#             neighbor[j][0] += difference
#
#             neighbors.append(neighbor)
#
#     return neighbors
def get_neighbors(solution, i):
    start = time()
    neighbors = []
    solution.sort(key=lambda x: x[0], reverse=True)

    # with Pool(cpu_count()) as p:
    #     for i in range(len(solution[0][1])):
    #         neighbors.append(p.apply(algorithms.get_neighbor, args=(i, solution)))
    # with ThreadPoolExecutor(max_workers=12) as executor:
    #     for i in range(len(solution[0][1])):
    #         executor.submit(get_neighbor, i, solution, neighbors)

    # for every task in the longest process
    # swap it with every task in every other process that will make the longest process shorter
    # and the other process not longer than the longest process
    # longest_processor = solution[0][0]
    # # get one task from the longest processor
    # for i, longest_processor_task in enumerate(solution[0][1]):
    for _ in range(1):
        # for every other processor get its length and task list
        for j, [processor_length, other_processor_tasks] in enumerate(solution[1:], start=1):
            # if processor have the same length as longest processor go to next processor
            # for every task in that processor check if it's shorter than the longest processor task
            neighbor = deepcopy(solution)
            task = neighbor[0][1].pop(i)
            neighbor[j][1].append(task)
            # neighbor[0][1].sort(reverse=True)
            neighbor[j][1].sort(reverse=True)
            #     # update processor length
            neighbor[0][0] -= task
            neighbor[j][0] += task

            neighbors.append(neighbor)
            for k, other_processor_task in enumerate(other_processor_tasks):
                neighbor = deepcopy(solution)
                difference = neighbor[0][1][i] - neighbor[j][1][k]
                neighbor[0][1][i], neighbor[j][1][k] = neighbor[j][1][k], neighbor[0][1][i]

                neighbor[0][1].sort(reverse=True)
                neighbor[j][1].sort(reverse=True)
                # update processor length
                neighbor[0][0] -= difference
                neighbor[j][0] += difference

                neighbors.append(neighbor)
            #
            #     for l in range(k+1, len(other_processor_tasks)):
            #         # swap tasks
            #         neighbor = deepcopy(solution)
            #         neighbor[0][1].append(neighbor[j][1][k])
            #         neighbor[0][1].append(neighbor[j][1][l])
            #         neighbor[j][1].pop(l)
            #         neighbor[j][1].pop(k)
            #
            #         neighbor[j][1].append(neighbor[0][1][i])
            #         neighbor[0][1].pop(i)
            #         #
            #         # neighbor[0][1][i], neighbor[j][1][k] = neighbor[j][1][k]+neighbor[j][1][l], neighbor[0][1][i]
            #         # neighbor[j][1].pop(l)
            #
            #         neighbor[0][1].sort(reverse=True)
            #         neighbor[j][1].sort(reverse=True)
            #         # update processor length
            #         neighbor[0][0] = sum(neighbor[0][1])
            #         neighbor[j][0] = sum(neighbor[j][1])
            #
            #         neighbors.append(neighbor)

    # best algorithm so far
    # longest_processor = solution[0][0]
    # # get one task from the longest processor
    # for i, longest_processor_task in enumerate(solution[0][1]):
    #     # for every other processor get its length and task list
    #     for j, [processor_length, other_processor_tasks] in enumerate(solution[1:], start=1):
    #         # if processor have the same length as longest processor go to next processor
    #         if processor_length + 1 < longest_processor:
    #             # for every task in that processor check if it's shorter than the longest processor task
    #             for k, other_processor_task in enumerate(other_processor_tasks):
    #                 # if other_processor_task == longest_processor_task:
    #                 #     continue
    #                 # if other_processor_task >= longest_processor_task:
    #                 #     continue
    #
    #                 # swap tasks
    #                 neighbor = deepcopy(solution)
    #                 neighbor[0][1][i], neighbor[j][1][k] = neighbor[j][1][k], neighbor[0][1][i]
    #
    #                 neighbor[0][1].sort(reverse=True)
    #                 neighbor[j][1].sort(reverse=True)
    #                 # update processor length
    #                 neighbor[0][0] = sum(neighbor[0][1])
    #                 neighbor[j][0] = sum(neighbor[j][1])
    #
    #                 neighbors.append(neighbor)

    # longest_processor = solution[0][0]
    # print("longest_processor", longest_processor)
    # get one task from the longest processor
    # for i, longest_processor_task in enumerate(solution[0][1]):
    #     # for every other processor get its length and task list
    #     for j, [processor_length, other_processor_tasks] in enumerate(solution[1:], start=1):
    #         # put it in the end of the other processor
    #         # swap tasks
    #         neighbor = deepcopy(solution)
    #         neighbor[0][1].pop(i)
    #         neighbor[j][1].append(longest_processor_task)
    #         neighbor[j][1].sort(reverse=True)
    #
    #         # update processor length
    #         neighbor[0][0] = sum(neighbor[0][1])
    #         neighbor[j][0] = sum(neighbor[j][1])
    #
    #         neighbors.append(neighbor)

    return time() - start, neighbors


def tabu_search(processors: int, tasks: list, max_iterations: int, tabu_list_size: int, time_limit: int = 60 * 5,
                draw: bool = False):
    """
    Algorym Tabu
    :param processors: liczba procesorow
    :param tasks: lista procesow
    :param max_iterations: liczba iteracji
    :param tabu_list_size: długość listy tabu
    :return: (dlugosc wykonywania procesow, czas wykonania, lista 2d z procesami na procesorach)
    """
    # generate initial solution using greedy algorith with reverse sorting of tasks
    optimum = int(math.ceil(sum(tasks) / processors))
    greedy_scheduling_time, initial_solution = greedy(processors, tasks, pre_sort=True)[1:]
    print("Initial solution:")
    print(*initial_solution, sep="\n")
    best_solution = initial_solution
    current_solution = initial_solution
    tabu_list = []
    full_neighbour_finding_time = 0

    print("Optimum: ", optimum)
    # visualize_schedule(initial_solution)
    start = time()
    for iteration in range(max_iterations):
        # print("generating neighbors")
        # start_generation = time()
        # print("generated neighbors in", time()-start_generation, "s")
        if draw:
            visualize_schedule(current_solution)
            print("generated plot")
        fitness_best_solution = objective_function(best_solution)
        best_neighbor = None
        best_neighbor_fitness = (float('inf'), float('inf'), float('inf'), float('inf'))
        current_solution.sort(key=lambda x: x[0], reverse=True)
        for i in range(len(current_solution[0][1])):
            neighbor_finding_time, neighbors = get_neighbors(current_solution, i)
            full_neighbour_finding_time += neighbor_finding_time
            for neighbor in neighbors:
                if not instances_are_equal(neighbor, tabu_list):
                    neighbor_fitness = objective_function(neighbor)
                    if neighbor_fitness < best_neighbor_fitness:
                        best_neighbor = neighbor
                        best_neighbor_fitness = neighbor_fitness

                    if neighbor_fitness[0] < fitness_best_solution[0] or \
                            neighbor_fitness[0] == fitness_best_solution[0] and \
                            neighbor_fitness[1] < fitness_best_solution[1]:
                        print("skipped")
                        break
            else:
                continue
            break

        # print("skipped")
        if best_neighbor is None:
            # No non-tabu neighbors found,
            # terminate the search
            print("No non-tabu neighbors found")
            break

        current_solution = best_neighbor
        tabu_list.append(sorted(best_neighbor))
        # if instances_are_equal(tabu_list[0], tabu_list[1:]):
        #     print("Something went wrong")
        if len(tabu_list) > tabu_list_size:
            # Remove the oldest entry from the
            # tabu list if it exceeds the size
            tabu_list.pop(0)

        print("Current best neighbor: ", objective_function(best_neighbor), "Current best solution: ",
              objective_function(best_solution))
        print("Current iteration: ", iteration)
        if objective_function(best_neighbor) < objective_function(best_solution):
            # Update the best solution if the
            # current neighbor is better
            print("Found better solution: {}", objective_function(best_neighbor))
            best_solution = best_neighbor

        # if time() - start > time_limit:
        #     print("Time limit reached, time: ", time() - start, "s")
        #     break
        #
        # if objective_function(best_solution)[0] == optimum:
        #     print("Found optimum: ", objective_function(best_solution)[0], "in iteration: ", iteration)
        #     break
    tabu_algorithm_time = time() - start

    return best_solution, greedy_scheduling_time, full_neighbour_finding_time, tabu_algorithm_time
