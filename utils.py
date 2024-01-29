import matplotlib.pyplot as plt
import pandas as pd


def visualize_schedule(schedule):
    """
    Visualize schedule
    :param schedule: list of processors with tasks
    """

    processors = len(schedule)
    tasks = []

    for i in range(processors):
        task_sum = 0
        for task in schedule[i][1]:
            tasks.append((f"P{i+1}", task_sum, task_sum + task))
            # schedule[i][j] = (i, schedule[i][j][0], schedule[i][j][1])
            task_sum += task

    tasks.sort(key=lambda x: x[2]-x[1])
    tasks.sort(key=lambda x: int(x[0][1:]))
    df = pd.DataFrame(tasks, columns=['Processor', 'Start', 'End'])

    plt.figure(figsize=(10, 6))
    for i, task in df.iterrows():
        color = 'C' + str((task['End'] - task['Start']) % 10)
        plt.barh(
            task['Processor'], task['End'] - task['Start'],
            left=task['Start'],
            color=color,
            alpha=0.7,
            edgecolor='w',
            linewidth=2
        )

    plt.xlabel('Time')
    plt.ylabel('Processor')
    # plt.title('Processor schedule')
    plt.grid(axis='x')
    plt.show(block=False)


def tabu_neighbor(neighbor, tabu_list):
    """
    Check if neighbor is in tabu list
    :param neighbor: neighbor to check
    :param tabu_list: tabu list

    :return: is neighbor in tabu list
    """
    if sorted(neighbor) in tabu_list:
        return True

    return False
