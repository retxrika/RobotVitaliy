from views import *
from models import *

if __name__ == '__main__':
    robotV = RobotV()
    print_robot(robotV, 'Robot creating')
    robotVita = RobotVita(robotV)
    print_robot(robotVita, 'Robot learning')
    robotVitaly = RobotVitaliy(robotVita)
    print_robot(robotVitaly, 'Robot working')
