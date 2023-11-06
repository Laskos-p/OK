from algorithms import *
from generator import *

print("1 - wprowadzanie danych z pliku")
print("2 - wprowadzanie danych z generatora")

match input("wybor: "):
    case "1":
        data = []
        with open("dane.txt", "r") as file:
            for line in file:
                if line[-1] == "\n":
                    line = line[:-1]
                data.append(line)

        # with open("dane.txt", "r") as file:
        #     processors = int(file.readline())
        #     tasks = list(map(int, file.readlines()))

        # print(processors, tasks)
        #
        processors = int(data[0])
        tasks = [int(el) for el in data[1].split(" ")]
    case "2":
        processors = int(input("liczba procesorow: "))
        num_tasks = int(input("liczba zadan: "))
        task_min_time = int(input("minimalny czas trwania zadania: "))
        task_max_time = int(input("maksymalny czas trwania zadania: "))

        tasks = generate(
            num_tasks,
            task_min_time,
            task_max_time
        )


print("1 - algorytm zachlanny")
print("2 - ")
match input("wybor: "):
    case "1":
        processor_time, execution_time, proc_list = greedy(processors, tasks.copy())
        print("czas wykonania:", execution_time, "s")
        print("najdłuższy czas wykorzystania procesora:", processor_time)
        print("czas wykorzystania procesorów:", proc_list)

    case "2":
        exit(0)


# print(processors, tasks)
#
# proc = [1 for i in range(processors)]
# t = 0
#
# while proc != [0]*processors:
#     for i in range(processors):
#         if proc[i] > 0:
#             proc[i] -= 1
#         if proc[i] == 0 and tasks != []:
#             proc[i] += tasks[0]
#             tasks.pop(0)
#     print("w chwili t = ", t, proc, tasks)
#     t += 1
#
# print("zakonczono przydzial procesow w czasie t = ", t)
