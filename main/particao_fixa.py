import time
from enum import Enum
from random import randint
from input_handler import InputHandler
from model.memory_partition import Partition
from model.process import Process

next_fit_last_index = 0

class AllocationAlgorithmEnum (Enum):
    FIRST_FIT = 1
    NEXT_FIT = 2
    BEST_FIT = 3
    WORST_FIT = 4

def print_memory_array(memory_array):
    rep = '['

    if len(memory_array) > 0:
        for partition in memory_array:
            rep = rep + str(partition) + ','
        rep = rep[:-1]

    rep = rep + ']'

    print(rep)


def read_partition_mock():
    partitions = []

    with open('../partition_size.txt') as file:

        lines = file.read().splitlines()

        for line in lines:
            if line[0] != '#':
                sizes = line.split(',')
                for data in sizes:
                    partitions.append(Partition(int(data)))

                break

    return partitions


def read_processes_mock():
    processes = []

    with open('../mock.txt') as file:
        lines = file.read().splitlines()

        for line in lines:
            data = line.split(',')

            name = data[0]
            id = data[1]
            size = int(data[2])

            processes.append(Process(id, size, name))

    return processes


def random_swap_out(partitioned_memory_array, minimum_size):

    while True:
        partition_address = randint(0, len(partitioned_memory_array) - 1)
        if partitioned_memory_array[partition_address].size >= minimum_size:
            process = partitioned_memory_array[partition_address].process
            partitioned_memory_array[partition_address].fragmented = False
            partitioned_memory_array[partition_address].process = None
            break

    return process


def get_external_fragmentation(partitioned_memory_array):
    acc = 0

    for partition in partitioned_memory_array:
        if partition.process is not None:
            acc = acc + (partition.size - partition.process.size)
        else:
            acc = acc + partition.size

    return acc


def first_fit(partitioned_memory_array, processes, process):
    for idx, partition in enumerate(partitioned_memory_array):
        if partition.process is None and process.size <= partition.size:
            partition.process = process
            if partition.size != process.size:
                partition.fragmented = True
            break

        if idx == len(partitioned_memory_array) - 1:  # Não há partição disponível para alocação
            processes.insert(0, process)  # Adicionando processo escolhido para alocação de volta na memória secundária

            process = random_swap_out(partitioned_memory_array, process.size)
            processes.insert(len(processes),
                             process)  # Adicionando processo escolhido para swap out de volta na memória secundária
            print('Memória cheia!')
            print(str(process) + ' foi retirado da memória principal e adicionado a memória secundária.')


def next_fit(partitioned_memory_array, processes, process):

    global next_fit_last_index

    next_fit_last_index = (next_fit_last_index + 1) % len(partitioned_memory_array)  # next index!

    for index in range(0, len(partitioned_memory_array)):
        adjusted_address = (next_fit_last_index + index) % len(partitioned_memory_array)
        partition = partitioned_memory_array[adjusted_address]

        if partition.process is None and process.size <= partition.size:
            partition.process = process
            if partition.size != process.size:
                partition.fragmented = True
            next_fit_last_index = adjusted_address
            break

        if index == (len(partitioned_memory_array) - 1):  # Não há partição disponível para alocação
            processes.insert(0, process)  # Adicionando processo escolhido para alocação de volta na memória secundária

            process = random_swap_out(partitioned_memory_array, process.size)
            processes.insert(len(processes),
                             process)  # Adicionando processo escolhido para swap out de volta na memória secundária
            print('Memória cheia!')
            print(str(process) + ' foi retirado da memória principal e adicionado a memória secundária.')
            next_fit_last_index = adjusted_address


def best_fit(partitioned_memory_array, processes, process):
    best_choice = None

    for idx, partition in enumerate(partitioned_memory_array):
        if partition.process is None and process.size <= partition.size:
            if best_choice is None:
                best_choice = partition
            else:
                if best_choice.size > partition.size:
                    best_choice = partition

        if idx == len(partitioned_memory_array) - 1 and best_choice is None:  # Não há partição disponível para alocação
            processes.insert(0, process)  # Adicionando processo escolhido para alocação de volta na memória secundária

            process = random_swap_out(partitioned_memory_array, process.size)
            processes.insert(len(processes),
                             process)  # Adicionando processo escolhido para swap out de volta na memória secundária
            print('Memória cheia!')
            print(str(process) + ' foi retirado da memória principal e adicionado a memória secundária.')

            return

    best_choice.process = process
    if best_choice.size != process.size:
        best_choice.fragmented = True


def worst_fit(partitioned_memory_array, processes, process):
    worst_choice = None

    for idx, partition in enumerate(partitioned_memory_array):
        if partition.process is None and process.size <= partition.size:
            if worst_choice is None:
                worst_choice = partition
            else:
                if worst_choice.size < partition.size:
                    worst_choice = partition

        if idx == len(partitioned_memory_array) - 1 and worst_choice is None:  # Não há partição disponível para alocação
            processes.insert(0, process)  # Adicionando processo escolhido para alocação de volta na memória secundária

            process = random_swap_out(partitioned_memory_array, process.size)
            processes.insert(len(processes),
                             process)  # Adicionando processo escolhido para swap out de volta na memória secundária
            print('Memória cheia!')
            print(str(process) + ' foi retirado da memória principal e adicionado a memória secundária.')

            return

    worst_choice.process = process
    if worst_choice.size != process.size:
        worst_choice.fragmented = True


def main():
    print('PARTIÇÃO FIXA\n')
    print('Escolha o algoritmo de alocação: ')
    print('(1) - First Fit')
    print('(2) - Next Fit')
    print('(3) - Best Fit')
    print('(4) - Worst Fit')

    allocation_algorithm = AllocationAlgorithmEnum(InputHandler.int_input('Digite sua escolha: ', (1, 4)))

    partitioned_memory_array = read_partition_mock()
    print('O tamanho total da memória física é de ' + str(sum(map((lambda p: p.size), partitioned_memory_array))) + ' bytes')

    n_partitions = len(partitioned_memory_array)
    print('Há ' + str(n_partitions) + ' partições na memória física.')
    print('\n')
    print_memory_array(partitioned_memory_array)
    time.sleep(5)

    processes = read_processes_mock()

    while processes:
        print('\n\n\n\n\n\n\n\n\n')
        process = processes.pop(0)

        print('Processo a ser alocado: ' + str(process))
        print('Situação atual da memória')
        print_memory_array(partitioned_memory_array)
        print('Fragmentação externa: ' + str(get_external_fragmentation(partitioned_memory_array)) + ' bytes')
        print('\n\n')

        if process.size > max(map((lambda p: p.size), partitioned_memory_array)):
            print('Não existe partição grande o suficiente para alocar este processo.')

        else:
            if allocation_algorithm == AllocationAlgorithmEnum.FIRST_FIT:
                first_fit(partitioned_memory_array, processes, process)
            elif allocation_algorithm == AllocationAlgorithmEnum.NEXT_FIT:
                next_fit(partitioned_memory_array, processes, process)
            elif allocation_algorithm == AllocationAlgorithmEnum.BEST_FIT:
                best_fit(partitioned_memory_array, processes, process)
            elif allocation_algorithm == AllocationAlgorithmEnum.WORST_FIT:
                worst_fit(partitioned_memory_array, processes, process)

        print_memory_array(partitioned_memory_array)
        print('Fragmentação externa: ' + str(get_external_fragmentation(partitioned_memory_array)) + ' bytes')
        time.sleep(5)
