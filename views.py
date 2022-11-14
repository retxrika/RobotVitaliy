import shutil
import time
import os

from texttable import Texttable
from colorama import init, Fore
from models import AbstractRobot, AbstractBuilding, House, Barn
from progress.bar import ChargingBar

def clear_cmd():
    os.system('cls')

def print_loading(msg_process : str):
    clear_cmd()
    bar = ChargingBar(Fore.BLUE + msg_process, max=100, 
                        suffix=Fore.GREEN + '%(percent)d%%', fill=Fore.YELLOW + '█')
    for i in range(100):
        bar.next()
        time.sleep(0.02)
    clear_cmd()

# Возвращает форматированную строку ошибки.
def get_error(text : str):
    return '\033[31m{}\033[0m'.format('ERROR: ' + text + '! Try again...')

def input_int(msg : str, 
              min : int = None, 
              max : int = None
) -> int:
    invalid_input_err = 'Invalid input'
    out_range_err = 'The number is not in the given range'

    while True:
        try:
            num = int(input(msg))
        except:
            print(get_error(invalid_input_err))
            continue
        
        if min != None and min > num:
            print(get_error(out_range_err))
            continue
        
        if max != None and max < num:
            print(get_error(out_range_err))
            continue
        return num

def input_char(msg : str, *chars):
    chars_text = ', '.join(chars)
    invalid_input_err = f'Character must be one of {chars_text}'

    while True:
        char = input(Fore.YELLOW + msg).lower()

        if char not in chars:
            print(get_error(invalid_input_err))
            continue
        return char

def print_table(robot : AbstractRobot):
    table = Texttable()
    table.add_row(['ID', 'Название', 'Количество этажей'])
    for i in range(len(robot._buildings)):
        table.add_row([str(i + 1), str(robot._buildings[i]), robot._buildings[i].get_count_floors()])
    
    print(table.draw())
    print()

def print_build(robot: AbstractRobot,
                type_build: AbstractBuilding, 
                msg_done: str, 
                msg_process: str):
    clear_cmd()
    if type_build == House:
        count_floors = input_int('Укажите количество этажей: ', 1)
        robot.build_house(count_floors)
    else:
        robot.build_barn() 
    print_loading(msg_process)
    print_header(msg_done)
    print_continue(center=False)

def print_change_count_floors(robot: AbstractRobot,
                            msg_done: str, 
                            msg_process: str,
                            add: bool = True):
    clear_cmd()
    if add:
        print_header('добавление этажа к постройке')
    else:
        print_header('снос верхнего этаже у постройки')
    print_table(robot)
    
    while True:
        id_build = input_int('Укажите номер постройки: ', 1, len(robot._buildings))

        building = robot._buildings[id_build - 1]
        if isinstance(building, Barn):
            print(get_error('The number of floors of barns cannot be changed'))
            continue
        break

    if add:
        robot.add_floor(building)
    else:
        robot.demolish_floor(building)

        if building.get_count_floors() == 0:
            robot._buildings.remove(building)
    print_loading(msg_process)
    print_header(msg_done)
    print_continue()

def print_test_mode(robot : AbstractRobot):
    count_funs = len(robot._functionality)

    while True:
        clear_cmd()
        print_header('Test mode')
        
        if len(robot._buildings) != 0:
            print_table(robot)
        
        print('Выберите требуемую функцию для тестирования:')
        
        for i in range(count_funs):
            print(f'{i + 1} - {robot._functionality[i].capitalize()}')
        print(str(count_funs + 1) + ' - Выйти из режима')
        
        num_fun = input_int('- ', 1, len(robot._functionality) + 1)

        if num_fun == len(robot._functionality) + 1:
            break

        match num_fun:
            case 1:
                print_build(
                    robot=robot,
                    type_build=House,
                    msg_done='Дом построен!', 
                    msg_process='House creating',
                )
            case 2:
                print_build(
                    robot=robot,
                    type_build=Barn, 
                    msg_done='Сарай построен!', 
                    msg_process='Barn creating',
                )
            case 3:
                print_change_count_floors(
                    robot=robot,
                    msg_process='Adding a floor',
                    msg_done='Этаж добавлен!',
                )
            case 4:
                print_change_count_floors(
                    robot=robot,
                    msg_process='Demolition of a floor',
                    msg_done='Этаж снесен!',
                    add=False,
                )

def print_continue(center : bool = True):
    width = shutil.get_terminal_size().columns

    print()
    print(Fore.YELLOW + 'Press enter for continue...'.center(width))
    input()    

def print_header(text : str):
    text = text.upper() + '\n'
    width = shutil.get_terminal_size().columns
    print(Fore.GREEN + text.center(width))

def print_main_page(robot : AbstractRobot, msg_process : str):
    init(autoreset=True)
    
    print_loading(msg_process + ':')

    lines = str(robot).split('\n')
    width = shutil.get_terminal_size().columns
    print_header('Information about robot')
    for line in lines:
        print(line.center(width))
    
    if len(robot._functionality) != 0:
        print(Fore.YELLOW + '\nВойти в режим тестирования робота? y/n: ')
        char = input_char(': ', 'y', 'n', 'д', 'н')

        if char in ('y', 'д'):
            print_test_mode(robot)
        clear_cmd()
    else:
        print_continue()
        clear_cmd()