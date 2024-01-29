from algorithms import *
from generator import *

print("1 - input from file")
print("2 - input from generator")
match input("choice: "):
    case "1":
        data = []
        file_name = input("Type file name with extension: ")
        with open(file_name, "r") as file:
            processors = int(file.readline())
            _ = int(file.readline())
            tasks = list(map(int, file.readlines()))

        print(processors, tasks)

    case "2":
        processors = int(input("Number of processors: "))
        num_tasks = int(input("Number of tasks: "))
        task_min_time = int(input("Shortest possible task time: "))
        task_max_time = int(input("Longest possible task time: "))

        tasks = generate(
            num_tasks,
            task_min_time,
            task_max_time
        )

        with open(f"generator_n{num_tasks}", "w") as f:
            f.write(str(processors) + "\n")
            f.write(str(num_tasks) + "\n")
            for task in tasks:
                f.write(str(task) + "\n")

    case _:
        print("Wrong input")
        exit(1)

print("1 - greedy algorithm")
print("2 - tabu search algorithm")
match input("choice: "):
    case "1":
        processor_time, execution_time, proc_list = greedy(processors, tasks.copy())
        print("Time taken to find solution: ", execution_time, "s")
        print("Longest processor time: ", processor_time)
        print("Processor list: ", *proc_list, sep="\n")

    case "2":
        iterations = int(input("Number of iterations: "))
        tabu_list_size = int(input("Length of tabu list: "))
        check_tasks = sorted(tasks.copy())
        tasks_sum = sum(tasks)

        tabu_output = tabu_search(processors, tasks, iterations, tabu_list_size, draw=False)
        tabu_solution, greedy_scheduling_time, full_neighbour_fining_time, tabu_algorithm_time = tabu_output

        # print all scheduled tasks
        print("Tabu solution:", *tabu_solution, sep="\n")
        print("Longest task: ", max(tabu_solution, key=lambda x: x[0]))
        print("Time to generate initial solution: ", greedy_scheduling_time)
        print("Time to find spent to find all neighbours: ", full_neighbour_fining_time)
        print("Time taken by tabu algorithm: ", tabu_algorithm_time - full_neighbour_fining_time)
        print("Time taken to find solution: ", greedy_scheduling_time + tabu_algorithm_time)

        # check if all tasks are present in solution
        print("Verifying solution...")
        tabu_tasks = [task for process in tabu_solution for task in process[1]]
        print(sorted(tabu_tasks) == check_tasks)

    case _:
        print("Wrong input")
        exit(1)
