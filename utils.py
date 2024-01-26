import matplotlib.pyplot as plt
import pandas as pd


def visualize_schedule(schedule):
    processors = len(schedule)
    tasks = []
    for i in range(processors):
        task_sum = 0
        for task in schedule[i][1]:
            tasks.append((f"Processor{i+1}", task_sum, task_sum + task))
            # schedule[i][j] = (i, schedule[i][j][0], schedule[i][j][1])
            task_sum += task

    df = pd.DataFrame(tasks, columns=['Processor', 'Start', 'End'])

    plt.figure(figsize=(10, 6))
    for i, task in df.iterrows():
        plt.barh(task['Processor'], task['End'] - task['Start'], left=task['Start'], alpha=0.6)

    plt.xlabel('Time')
    plt.ylabel('Processor')
    plt.title('Processor schedule')
    plt.grid(axis='x')
    plt.show(block=False)


def instances_are_equal(neighbor, tabu_list):
    # print("Neighbor:", *neighbor, sep="\n")
    # print("Tabu list:", *tabu_list, sep="\n")
    for tabu_solution in tabu_list:
        equalities = 0
        for neighbor_solution in neighbor:
            if neighbor_solution in tabu_solution:
                equalities += 1

        if equalities == len(neighbor):
            return True

    return False
