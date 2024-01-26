from time import time
from copy import deepcopy
# from collections import defaultdict
from utils import visualize_schedule, instances_are_equal


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
    longest_processor = max(proc_list, key=lambda x: x[0])[0]
    longest_processors = len([processor for processor in proc_list if processor[0] == longest_processor])
    # return max(proc_list, key=lambda x: x[0])[0]
    optimal_length_processors = len([processor for processor in proc_list if processor[0] == 977])
    return (longest_processor, longest_processors, -optimal_length_processors)

def get_neighbors(solution):
    start = time()
    neighbors = []
    solution.sort(key=lambda x: x[0], reverse=True)

    # for every task in the longest process
    # swap it with every task in every other process that will make the longest process shorter
    # and the other process not longer than the longest process
    longest_processor = solution[0][0]
    # get one task from the longest processor
    for i, longest_processor_task in enumerate(solution[0][1]):
        # for every other processor get its length and task list
        for j, [processor_length, other_processor_tasks] in enumerate(solution[1:], start=1):
            # if processor have the same length as longest processor go to next processor
            # for every task in that processor check if it's shorter than the longest processor task
            for k, other_processor_task in enumerate(other_processor_tasks):
                neighbor = deepcopy(solution)
                neighbor[0][1][i], neighbor[j][1][k] = neighbor[j][1][k], neighbor[0][1][i]

                neighbor[0][1].sort(reverse=True)
                neighbor[j][1].sort(reverse=True)
                # update processor length
                neighbor[0][0] = sum(neighbor[0][1])
                neighbor[j][0] = sum(neighbor[j][1])

                neighbors.append(neighbor)

                for l in range(k+1, len(other_processor_tasks)):
                    # swap tasks
                    neighbor = deepcopy(solution)
                    neighbor[0][1].append(neighbor[j][1][k])
                    neighbor[0][1].append(neighbor[j][1][l])
                    neighbor[j][1].pop(l)
                    neighbor[j][1].pop(k)

                    neighbor[j][1].append(neighbor[0][1][i])
                    neighbor[0][1].pop(i)
                    #
                    # neighbor[0][1][i], neighbor[j][1][k] = neighbor[j][1][k]+neighbor[j][1][l], neighbor[0][1][i]
                    # neighbor[j][1].pop(l)

                    neighbor[0][1].sort(reverse=True)
                    neighbor[j][1].sort(reverse=True)
                    # update processor length
                    neighbor[0][0] = sum(neighbor[0][1])
                    neighbor[j][0] = sum(neighbor[j][1])

                    neighbors.append(neighbor)

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

    return time()-start, neighbors


def tabu_search(processors: int, tasks: list, max_iterations: int, tabu_list_size: int, draw: bool = False):
    """
    Algorym Tabu
    :param processors: liczba procesorow
    :param tasks: lista procesow
    :param max_iterations: liczba iteracji
    :param tabu_list_size: długość listy tabu
    :return: (dlugosc wykonywania procesow, czas wykonania, lista 2d z procesami na procesorach)
    """
    # generate initial solution using greedy algorith with reverse sorting of tasks
    greedy_scheduling_time, initial_solution = greedy(processors, tasks, pre_sort=True)[1:]
    print("Initial solution:")
    print(*initial_solution, sep="\n")
    best_solution = initial_solution
    current_solution = initial_solution
    tabu_list = []
    full_neighbour_finding_time = 0

    # visualize_schedule(initial_solution)
    start = time()
    for iteration in range(max_iterations):
        print("generating neighbors")
        neighbor_finding_time, neighbors = get_neighbors(current_solution)
        if draw:
            visualize_schedule(current_solution)
            print("generated plot")
        full_neighbour_finding_time += neighbor_finding_time
        best_neighbor = None
        best_neighbor_fitness = (float('inf'), float('inf'), float('inf'))

        for neighbor in neighbors:
            if not instances_are_equal(neighbor, tabu_list):
                neighbor_fitness = objective_function(neighbor)
                if neighbor_fitness < best_neighbor_fitness:
                    best_neighbor = neighbor
                    best_neighbor_fitness = neighbor_fitness

            else:
                print("instance already in tabu list")

        if best_neighbor is None:
            # No non-tabu neighbors found,
            # terminate the search
            print("No non-tabu neighbors found")
            break

        current_solution = best_neighbor
        tabu_list.append(best_neighbor)
        # if instances_are_equal(tabu_list[0], tabu_list[1:]):
        #     print("Something went wrong")
        if len(tabu_list) > tabu_list_size:
            # Remove the oldest entry from the
            # tabu list if it exceeds the size
            tabu_list.pop(0)

        print("Current best neighbor: ", objective_function(best_neighbor), "Current best solution: ", objective_function(best_solution))
        print("Current iteration: ", iteration)
        if objective_function(best_neighbor) < objective_function(best_solution):
            # Update the best solution if the
            # current neighbor is better
            print("Found better solution: {}", objective_function(best_neighbor))
            best_solution = best_neighbor

    tabu_algorithm_time = time() - start

    return best_solution, greedy_scheduling_time, full_neighbour_finding_time, tabu_algorithm_time
