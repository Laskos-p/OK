from algorithms import *
from generator import *

print("1 - wprowadzanie danych z pliku")
print("2 - wprowadzanie danych z generatora")

match input("wybor: "):
    case "1":
        data = []
        # with open("dane.txt", "r") as file:
        #     for line in file:
        #         if line[-1] == "\n":
        #             line = line[:-1]
        #         data.append(line)
        file_name = input("Podaj nazwę pliku z rozszerzeniem: ")
        with open(file_name, "r") as file:
            processors = int(file.readline())
            _ = int(file.readline())
            tasks = list(map(int, file.readlines()))

        print(processors, tasks)

        # processors = int(data[0])
        # tasks = [int(el) for el in data[1].split(" ")]
    case "2":
        processors = int(input("liczba procesorow: "))
        num_tasks = int(input("liczba zadan: "))
        task_min_time = int(input("minimalny czas trwania zadania: "))
        task_max_time = int(input("maksymalny czas trwania zadania: "))

        # tasks = RandomList(num_tasks, task_min_time, task_max_time)
        tasks = generate(
            num_tasks,
            task_min_time,
            task_max_time
        )

        with open("generator", "w") as f:
            f.write(str(processors) + "\n")
            f.write(str(num_tasks) + "\n")
            for task in tasks:
                f.write(str(task) + "\n")

print("1 - algorytm zachlanny")
print("2 - algorytm tabu")
print("3 - algorytm tabu z przeszukiwaniem pełnej listy sąsiedztwa")
print("4 - algorytm tabu z rysowaniem kolejnych instancji")
match input("wybor: "):
    case "1":
        # print(tasks.tasks)
        processor_time, execution_time, proc_list = greedy(processors, tasks.copy())
        print("czas wykonania:", execution_time, "s")
        print("najdłuższy czas wykorzystania procesora:", processor_time)
        print("czas wykorzystania procesorów:", *proc_list, sep='\n')

    case "2":
        iterations = int(input("Podaj liczbę iteracji: "))
        tabu_list_size = int(input("Podaj długość listy tabu: "))
        tabu_solution, greedy_scheduling_time, full_neighbour_fining_time, tabu_algorithm_time = tabu_search(processors, tasks, iterations, tabu_list_size)
        # print all scheduled task
        print("Tabu solution:", *tabu_solution, sep="\n")
        print("Longest task: ", max(tabu_solution, key=lambda x: x[0]))
        print("Time to generate initial solution: ", greedy_scheduling_time)
        print("Time to find spent to find all neighbours: ", full_neighbour_fining_time)
        print("Time taken by tabu algorithm: ", tabu_algorithm_time - full_neighbour_fining_time)
        print("Time taken to find solution: ", greedy_scheduling_time + full_neighbour_fining_time + tabu_algorithm_time)
    case "3":
        pass
    case "4":
        iterations = int(input("Podaj liczbę iteracji: "))
        tabu_list_size = int(input("Podaj długość listy tabu: "))
        tabu_solution, greedy_scheduling_time, full_neighbour_fining_time, tabu_algorithm_time = tabu_search(processors, tasks, iterations, tabu_list_size, draw=True)
        # print all scheduled task
        # print("Tabu solution:", *tabu_solution, sep="\n")
        print("Longest task: ", max(tabu_solution, key=lambda x: x[0]))
        print("Time to generate initial solution: ", greedy_scheduling_time)
        print("Time to find spent to find all neighbours: ", full_neighbour_fining_time)
        print("Time taken by tabu algorithm: ", tabu_algorithm_time - full_neighbour_fining_time)
        print("Time taken to find solution: ", greedy_scheduling_time + full_neighbour_fining_time + tabu_algorithm_time)