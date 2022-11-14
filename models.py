from typing import List


class OneMoreRobotException(Exception):
    def __str__(self) -> str:
        return 'Attempt to create one more robot'

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
        raise OneMoreRobotException

class AbstractBuilding():
    __count_floors : int = None

    def get_count_floors(self) -> int:
        return None

class House(AbstractBuilding):
    def __init__(self, count_floors):
        self.__count_floors = count_floors

    def add_floor(self):
        self.__count_floors += 1

    def demolish_floor(self):
        self.__count_floors -= 1

    def get_count_floors(self) -> int:
        return self.__count_floors

    def __str__(self) -> str:
        return 'Дом'

class Barn(AbstractBuilding):
    def __init__(self):
        self.__count_floors = 1

    def get_count_floors(self) -> int:
        return 1

    def __str__(self) -> str:
        return 'Сарай'

class AbstractRobot(metaclass = MetaSingleton):
    _serial_number   : str = 'АА001221-56'
    _name            : str = None
    _place           : str = None
    _functionality    : List = list()
    _buildings        : List[AbstractBuilding] = list()

    def build_house(self, count_floors : int):
        pass
    
    def build_barn(self) -> Barn:
        pass

    def add_floor(self, build : AbstractBuilding = None):
        pass
    
    def demolish_floor(self, build : AbstractBuilding = None):
        pass

    def __str__(self):
        functionality = 'Не имеется' if len(self._functionality) == 0 \
                                    else ',\n'.join(self._functionality).capitalize()

        return  f'Серийный номер: {self._serial_number}.\n' + \
                f'Наименование: {self._name}.\n' + \
                f'Место нахождения: {self._place}.\n' + \
                f'Функциональность: {functionality}.'

class RobotV(AbstractRobot):
    def __init__(self):
        self._name = 'В'
        self._place = 'Завод по созданию роботов'

class AbstractRobotDecorator(AbstractRobot):
    __robot : AbstractRobot = None

    def __init__(self, robot):
        self.__robot = robot
    
    def build_house(self, count_floors : int):
        self.__robot.build_house(count_floors=count_floors)
    
    def build_barn(self):
        self.__robot.build_barn()

    def add_floor(self, build : AbstractBuilding = None):
        self.__robot.add_floor(build=build)
    
    def demolish_floor(self, build : AbstractBuilding = None):
        self.__robot.demolish_floor(build=build)

class RobotVita(AbstractRobotDecorator):
    def __init__(self, robot):
        super().__init__(robot)
        self._name = 'Вита'
        self._place = 'Учебный центр для роботов'
        self._functionality.append('постройка домов')
        self._functionality.append('постройка сараев')

    def build_house(self, count_floors : int):
        self._buildings.append(House(count_floors))
    
    def build_barn(self):
        self._buildings.append(Barn())

class RobotVitaliy(AbstractRobotDecorator):
    def __init__(self, robot):
        super().__init__(robot)
        self._name = 'Виталий'
        self._place = 'Предприятие "ООО Кошмарик"'
        self._functionality.append('добавление этажа к постройке')
        self._functionality.append('снос верхнего этаже у постройки')

    def add_floor(self, build : AbstractBuilding = None):
        if isinstance(build, House):
            build.add_floor()
    
    def demolish_floor(self, build : AbstractBuilding = None):
        if isinstance(build, House):
            build.demolish_floor()