from dataclasses import dataclass
from typing import Dict, List, Tuple, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str = ''
    duration: float = float
    distance: float = float
    speed: float = float
    calories: float = float

    def get_message(self) -> str:
        """Возвращает информационное сообщение о тренировке."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'This source does not implement: spent_calories.'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_1: int = 18
    COEFF_2: int = 20

    def get_spent_calories(self) -> float:
        """Рассчет потраченных колорий для Бега."""
        spent_calories: float = ((
            self.COEFF_1
            * self.get_mean_speed()
            - self.COEFF_2)
            * self.weight / self.M_IN_KM
            * self.duration * self.M_IN_H)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_3: float = 0.035
    COEFF_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Подсчет калорий для тренировки Спортивная Ходьба."""
        spent_calories: float = ((
            self.COEFF_3 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.COEFF_4 * self.weight)
            * self.duration * self.M_IN_H)

        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    COEFF_5: float = 1.1
    COEFF_6: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Рассчет скорости плавания."""
        speed: float = (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Рассчет потраченных калорий для тренировки Плавание."""
        spent_calories: float = ((
            self.get_mean_speed()
            + self.COEFF_5)
            * self.COEFF_6 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}

    if workout_type not in training_types:
        raise ValueError('This type of training not found.')
    return training_types[workout_type](*data)


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
