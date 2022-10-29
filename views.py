import shutil
import time
import os

from colorama import init, Fore
from models import AbstractRobot
from progress.bar import ChargingBar

def print_loading(msg_process : str):
    bar = ChargingBar(Fore.BLUE + msg_process, max=100, 
                        suffix=Fore.GREEN + '%(percent)d%%', fill=Fore.YELLOW + '█')
    for i in range(100):
        bar.next()
        time.sleep(0.02)

def print_robot(robot : AbstractRobot, msg_process : str):
    init(autoreset=True)
    
    os.system('cls')
    print_loading(msg_process + ':')
    os.system('cls')

    lines = str(robot).split('\n')
    width = shutil.get_terminal_size().columns
    print(Fore.GREEN + 'INFORMATION ABOUT ROBOT\n'.center(width))
    for line in lines: # center
        print(line.center(width))

    print()
    print(Fore.YELLOW + 'Press enter for continue...'.center(width))
    input()
    os.system('cls')