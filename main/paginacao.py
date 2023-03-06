import configparser
import random
import time
from model.process import Process
from input_handler import InputHandler

PageFrameSize = 0
PhysicalMemorySize = 0
VirtualMemory = []
PhysicalMemory = []
PageTable = {}
PageMiss = 0
LRUReferencesThreshold = 0
ReferenceCounter = 0


def print_virtual_memory():
    global PageFrameSize, VirtualMemory

    rep = '['

    if len(VirtualMemory) > 0:
        for page in VirtualMemory:
            rep = rep + str(page) + ','
        rep = rep[:-1]

    rep = rep + ']'

    print(rep)


def print_physical_memory():
    global PhysicalMemory, PageFrameSize
    rep = '['

    if len(PhysicalMemory) > 0:
        for page in PhysicalMemory:
            rep = rep + str(page)

            if page is not None:
                rep = rep + 'frag?' + ('True:' + str(PageFrameSize - page.size) if page.size < PageFrameSize else 'False')

            rep = rep + ','
        rep = rep[:-1]

    rep = rep + ']'

    print(rep)


def read_memory_properties():
    config = configparser.RawConfigParser()
    config.read('virtual_memory.properties')

    global PageFrameSize, VirtualMemory, PhysicalMemorySize, PhysicalMemory, PageTable

    PageFrameSize = int(config.get('simulation', 'PageFrameSize'))
    virtual_memory_data = config.get('simulation', 'VirtualMemory').split(';')
    PhysicalMemorySize = int(config.get('simulation', 'PhysicalMemorySize'))

    for page in virtual_memory_data:
        page = page.split(',')
        process = Process(name=page[0], id=page[1], size=int(page[2]), pageId=page[3], lru_counter=0)
        VirtualMemory.append(process)
        PageTable[process] = None  # Inicialmente uma página virtual não está mapeada em nenhum frame na memória física

    PhysicalMemory = [None] * (PhysicalMemorySize // PageFrameSize)


def least_recently_used():
    global PhysicalMemory
    least_used = 0

    for idx, page in enumerate(PhysicalMemory[1:]):
        if page.lru_counter < PhysicalMemory[least_used].lru_counter:
            least_used = idx

    return least_used


def main():
    global PageTable, PhysicalMemory, PageMiss, LRUReferencesThreshold, ReferenceCounter

    print('PAGINAÇÃO')
    print('O algoritmo de substituição de página utilizado é o LRU')
    LRUReferencesThreshold = InputHandler.int_input('Digite o limite de referencias em que o contador do LRU será resetado: ')
    print()

    read_memory_properties()

    while True:

        if ReferenceCounter == LRUReferencesThreshold:  # Resetando contador de referências
            print('A quantidade de referências chegou ao limite de referências para resetar o LRU.')
            print('Resetando contador de referências!')
            ReferenceCounter = 0
            for page in PhysicalMemory:
                page.lru_counter = 0
            time.sleep(5)
            print('CONTADOR DE REFERÊNCIAS RESETADO!')
            time.sleep(2)
            print('\n\n\n\n\n')

        chosen_page = random.choice(list(PageTable.keys()))  # Escolha randômica por uma página virtual
        ReferenceCounter += 1

        print('Memória virtual')
        print_virtual_memory()
        print()

        print('Página solicitada: ' + str(chosen_page))
        print()

        print('Memória física pré-alocação')
        print_physical_memory()
        print()

        time.sleep(3)

        if PageTable[chosen_page] is None:  # Página virtual não está na memória física. PAGE MISS!
            PageMiss += 1
            print('PAGE MISS! ' + str(PageMiss))

            if None in PhysicalMemory:  # Há um frame de memória disponível para alocar
                for idx in range(0, len(PhysicalMemory)):
                    if PhysicalMemory[idx] is None:
                        PhysicalMemory[idx] = chosen_page
                        PageTable[chosen_page] = idx

                        print('Página alocada no endereço ' + str(idx))
                        PhysicalMemory[idx].lru_counter += 1
                        break

            else:  # Não há frame disponível para alocar. É preciso executar o algoritmo de substituição de página

                replacement_address = least_recently_used()
                PhysicalMemory[replacement_address].lru_counter = 0  # Página sofrerá swap-out, resetando contador de referências.
                PageTable[PhysicalMemory[replacement_address]] = None
                PhysicalMemory[replacement_address] = chosen_page
                PhysicalMemory[replacement_address].lru_counter += 1
                PageTable[chosen_page] = replacement_address
                print('Página no endereço ' + str(replacement_address) + ' foi substituída pela página solicitada')
                print()

            print('Memória física pós-alocação')
            print_physical_memory()
            print()

        else:
            print('PAGE FOUND!')
            PhysicalMemory[PageTable[chosen_page]].lru_counter += 1
            print('Lendo endereço ' + str(PageTable[chosen_page]) + ' da memória física.')
            print()

        time.sleep(5)
        print('\n\n\n')
