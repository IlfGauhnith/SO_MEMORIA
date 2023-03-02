import sys

from input_handler import InputHandler
from particao_fixa import main as particao_fixa_main
from paginacao import main as paginacao_main

if __name__ == '__main__':

    print('WINTERMUTE XXIII')
    print()

    print('Escolha o tipo de alocação de memória:')
    print('(0) - EXIT')
    print('(1) - Partições fixas')
    print('(2) - Paginação')

    menu_choice = InputHandler.int_input('Digite sua escolha: ', (0, 2))
    print('\n\n\n')

    if menu_choice == 1:
        particao_fixa_main()

    elif menu_choice == 2:
        paginacao_main()
