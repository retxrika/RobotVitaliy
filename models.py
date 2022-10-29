class OneMoreRobotException(Exception):
    def __str__(self):
        return 'Attempt to create one more robot'

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
            return cls._instances[cls]
        raise OneMoreRobotException

class AbstractRobot(metaclass = MetaSingleton):
    serial_number   : str   = 'АА001221-56'
    name            : str   = None   
    place           : str   = None
    functionality   : list  = list()

    def __str__(self):
        functionality = 'Не имеется' if len(self.functionality) == 0 \
                                    else ', '.join(self.functionality).capitalize()

        return  f'Серийный номер: {self.serial_number}.\n' + \
                f'Наименование: {self.name}.\n' + \
                f'Место нахождения: {self.place}.\n' + \
                f'Функциональность: {functionality}.'

class RobotV(AbstractRobot):
    def __init__(self):
        self.name = 'В'
        self.place = 'Завод по созданию роботов'

class AbstractRobotDecorator(AbstractRobot):
    robot : AbstractRobot

    def __init__(self, robot):
        self.robot = robot

class RobotVita(AbstractRobotDecorator):
    def __init__(self, robot):
        super().__init__(robot)
        self.name = 'Вита'
        self.place = 'Специальный учебный комплект первичного обучения роботов'
        self.functionality.append('постройка домов')
        self.functionality.append('постройка сараев')

class RobotVitaliy(AbstractRobotDecorator):
    def __init__(self, robot):
        super().__init__(robot)
        self.name = 'Виталий'
        self.place = 'Предприятие "ООО Кошмарик"'
        self.functionality.append('добавление этажа к постройке')
        self.functionality.append('снос верхнего этаже у постройки')
