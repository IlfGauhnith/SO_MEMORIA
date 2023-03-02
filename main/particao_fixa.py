import sys
import time
from random import randint

from input_handler import InputHandler
from model.memory_partition import Partition
from model.process import Process


def print_memory_array(memory_array):
    rep = '['

    if len(memory_array) > 0:
        for partition in memory_array:
            rep = rep + str(partition) + ','
        rep = rep[:-1]

    rep = rep + ']'

    print(rep)


def read_processes_mock():
    processes = []

    with open('mock.txt') as file:
        lines = file.read().splitlines()

        for line in lines:
            data = line.split(',')

            name = data[0]
            id = data[1]
            size = int(data[2])

            processes.append(Process(id, size, name))

    return processes


def random_swap_out(partitioned_memory_array):

    partition_address = randint(0, len(partitioned_memory_array) - 1)
    process = partitioned_memory_array[partition_address].process
    partitioned_memory_array[partition_address].fragmented = False
    partitioned_memory_array[partition_address].process = None

    return process


def get_external_fragmentation(partitioned_memory_array):
    acc = 0

    for partition in partitioned_memory_array:
        if partition.fragmented:
            acc = acc + (partition.size - partition.process.size)

    return acc


def main():
    print('PARTIÇÃO FIXA\n')

    memory_size = InputHandler.int_input('Digite o tamanho da memória em bytes: ', (1, sys.maxsize))
    partition_size = InputHandler.int_input('Digite o tamanho da partição em bytes: ', (1, memory_size))
    n_partitions = memory_size//partition_size

    print('A memória física foi dividida em ' + str(n_partitions) + ' partições de ' + str(partition_size) + ' bytes.')
    print(str(memory_size % partition_size) + ' bytes foram desperdiçados no particionamento.')
    time.sleep(5)

    partitioned_memory_array = [Partition(partition_size) for _ in range(0, n_partitions)]
    processes = read_processes_mock()

    while processes:
        print('\n\n\n\n\n\n\n\n\n')
        process = processes.pop(0)

        print('Processo a ser alocado: ' + str(process))
        print('Situação atual da memória')
        print_memory_array(partitioned_memory_array)
        print('\n\n')

        if process.size > partition_size:
            print('Tamanho do processo excede tamanho da partição, não é possível alocar.')

        else:
            for idx, partition in enumerate(partitioned_memory_array):
                if partition.process is None: # Encontrou partição vazia disponível para alocação
                    partition.process = process

                    if process.size != partition_size:
                        partition.fragmented = True

                    print('Processo alocado!')
                    break

                elif idx == len(partitioned_memory_array) - 1:  # Não há partição vazia disponível para alocação
                    processes.insert(0, process)  # Adicionando processo escolhido para alocação de volta na memória secundária

                    process = random_swap_out(partitioned_memory_array)
                    processes.insert(len(processes), process)  # Adicionando processo escolhido para swap out de volta na memória secundária
                    print(str(process) + ' foi retirado da memória principal e adicionado a memória secundária.')
        print_memory_array(partitioned_memory_array)
        print('Fragmentação externa: ' + str(get_external_fragmentation(partitioned_memory_array)) + ' bytes')
        time.sleep(5)
