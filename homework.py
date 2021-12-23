from typing import Dict, Type, List, Tuple


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.calories = calories
        self.speed = speed

    def get_message(self) -> str:
        return(
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20
    M_IN_H: int = 60
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        spent_calories = (
                (self.coeff_calorie_1 * self.get_mean_speed() - self.coeff_calorie_2)
                * self.weight / self.M_IN_KM * self.duration * self.M_IN_H)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3: float = 0.035
    coeff_calorie_4: float = 0.029
    coeff_calorie_5: float = 2
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_calories = (
                (self.coeff_calorie_3 * self.weight +
                 (self.get_mean_speed() ** self.coeff_calorie_5 // self.height) *
                 self.coeff_calorie_4 * self.weight) * self.duration * self.M_IN_H)

        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_5: float = 1.1
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000
    M_IN_H: int = 60
    coeff_calorie_6 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ):
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool /
                 self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        spent_calories = (
                (self.get_mean_speed() + self.coeff_calorie_5)
                * self.coeff_calorie_6 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
         }
    return dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
