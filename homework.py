from typing import Dict, List, Tuple, Union


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float, distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

    def __str__(self) -> str:
        return self.get_message()


class Training:
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
           Для каждого вида тренировки расчет отдельный"""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type: str = type(self).__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(training_type,
                           duration,
                           distance,
                           speed,
                           calories)

    def get_duration_minutes(self) -> float:
        duration_minutes: float = self.duration * 60
        return duration_minutes


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий на бег."""
        k_calor_1: int = 18
        k_calor_2: int = 20
        speed: float = super().get_mean_speed()
        duration_minutes = super().get_duration_minutes()
        spent_calor: float = ((k_calor_1 * speed - k_calor_2) * self.weight
                              / self.M_IN_KM * duration_minutes)
        return spent_calor


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий на спортивную ходьбу"""
        k_calor_3: float = 0.035
        k_calor_4: float = 0.029
        speed: float = super().get_mean_speed()
        duration_minutes: float = super().get_duration_minutes()
        spent_calor: float = ((k_calor_3 * self.weight + (speed**2
                              // self.height) * k_calor_4 * self.weight)
                              * duration_minutes)
        return spent_calor


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    LEN_STEP: float = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость для плавания"""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий на плавание"""
        k_calor_5: float = 1.1
        k_calor_6: int = 2
        speed: float = self.get_mean_speed()
        spent_calor: float = ((speed + k_calor_5)
                              * k_calor_6 * self.weight)
        return spent_calor


def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: Dict[str, type] = ({'SWM': Swimming,
                                  'RUN': Running,
                                  'WLK': SportsWalking})
    return workouts[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = Training.show_training_info(training)
    print(info)


if __name__ == '__main__':

    PackType = List[Tuple[str, List[Union[int, float]]]]
    packages: PackType = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
