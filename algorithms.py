from time import time


def greedy(processors: int, tasks: list) -> tuple:
    """
    Algorytm zachlanny
    :param proc: liczba procesorow
    :param tasks: lista procesow

    :return: (dlugosc wykonywania procesow, czas wykonania, lista 2d z procesami na procesorach)
    """
    proc = [0 for i in range(processors)]
    start = time()
    while tasks:
        proc.sort()
        proc[0] += tasks[0]
        tasks.pop(0)

    execution_time = time() - start
    processor_time = max(proc)

    return processor_time, execution_time, proc
