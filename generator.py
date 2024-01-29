from random import randint


def generate(
        tasks: int,
        task_min_time: int,
        task_max_time: int
):
    tasks = [randint(task_min_time, task_max_time) for _ in range(tasks)]
    return tasks
