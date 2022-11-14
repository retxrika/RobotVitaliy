from views import *
from models import *

if __name__ == '__main__':
    robotV = RobotV()
    print_main_page(robotV, 'Robot creating')
    robotVita = RobotVita(robotV)
    print_main_page(robotVita, 'Robot learning')
    robotVitaly = RobotVitaliy(robotVita)
    print_main_page(robotVitaly, 'Robot working')
