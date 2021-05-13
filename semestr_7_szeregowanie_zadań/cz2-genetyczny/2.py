from random import randint
import math
from numba import jit
import numpy as np

def create_gen_zero(population, mutation_flat, n, best_scheduled):
    gen_zero = np.full((population, n, 4), -1)
    # print(gen_zero)
    for entity in range(population):
        ns = np.array(best_scheduled)
        for _ in range(int(math.sqrt(n))):
            for mutation in range(mutation_flat):
                a, b = randint(0, n - 1), randint(0, n - 1)  # Choose tasks to swap
                ns[a], ns[b] = ns[b].copy(), ns[a].copy()
        gen_zero[entity] = ns
    return gen_zero


def crossover(s1, s2, n):
    ns = np.full((n, 4), -1)
    s1a, s1b = randint(0, n-1), randint(0, n-1)
    if s1a <= s1b:
        ns[s1a:s1b] = s1[s1a:s1b]
        used_taks = s1[s1a:s1b][:, 0]
    else:
        ns[s1a:] = s1[s1a:]
        ns[:s1b] = s1[:s1b]
        used_taks = np.concatenate((s1[:s1b][:, 0], s1[s1a:][:, 0]), axis=0)
    missing_tasks = []
    for i, task in enumerate(ns):
        if task[0] != -1:
            if s2[i][0] not in ns[:,0]:
                missing_tasks.append(s2[i])
            continue
        if s2[i][0] not in used_taks:
            ns[i] = s2[i]
    if len(missing_tasks) != 0:
        ns[np.where(ns[:, 0] == -1)] = missing_tasks
    print("NS", ns)
    return ns


def create_new_gen(prev, group_size, population, n, start_time_line, mutation_rate_percent, due_date):
    number_of_groups = int(len(prev) / group_size)
    groups = [[] for _ in range(number_of_groups)]
    for i in range(0, len(prev), group_size):
        groups[int(i / group_size)] = prev[i:i + group_size]
    new_seed = []
    for group in groups:
        _best_task = (-1, math.inf)
        for i, task in enumerate(group):
            _penalty = calculate_penalties(task, start_time_line, due_date)
            _best_task = (i, _penalty) if _penalty < _best_task[1] else _best_task
        new_seed.append(group[_best_task[0]])
    new_population = []
    nsl = len(new_seed)
    _best_penalty = math.inf
    _best_task = []
    for _ in range(population):
        new_task = crossover(new_seed[randint(0, nsl - 1)], new_seed[randint(0, nsl - 1)], n)
        break
        for _ in range(int(math.sqrt(n))):
            if randint(0, 100) < mutation_rate_percent:
                tasks_to_swap = (randint(0, n - 1), randint(0, n - 1))
                # tasks_to_swap = (randint(0, n-1), randint(0, n-1))  # Choose tasks to swap
                new_task[tasks_to_swap[0]], new_task[tasks_to_swap[1]] = new_task[tasks_to_swap[1]], new_task[
                    tasks_to_swap[0]]  # Mutate schedule

        new_population.append(new_task)
        _penalty = calculate_penalties(new_task, start_time_line, due_date)
        _best_penalty = _penalty if _penalty < _best_penalty else _best_penalty
        _best_task = new_task if _penalty == _best_penalty else _best_task

    print(_best_penalty, ', '.join([str(task['id']) for task in _best_task]))
    return new_population


def get_best(population, start_time_line, due_date):
    _best_task = (-1, math.inf)
    for i, task in enumerate(population):
        _penalty = calculate_penalties(task, start_time_line, due_date)
        _best_task = (i, _penalty) if _penalty < _best_task[1] else _best_task
    return population[i]


def run(n, k, h, ot, tpt, dd, bs, gv, stl):
    generation = create_gen_zero(population, mutation_flat, n, best_scheduled)
    for gen in range(generations):
        generation = create_new_gen(generation, 4, population, n, start_time_line, mutation_rate_percent, due_date)
    best_schedule = get_best(generation, start_time_line, due_date)
    return calculate_penalties(best_schedule, start_time_line, due_date), best_schedule
