from typing import Dict, List, Tuple, Union


class InfoMessage:
    """Info message about workout"""
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
        return (f'Training type: {self.training_type}; '
                f'Duration: {self.duration:.3f} ч.; '
                f'Distance: {self.distance:.3f} км; '
                f'Average speed: {self.speed:.3f} км/ч; '
                f'Kcalories lost: {self.calories:.3f}.')

    def __str__(self) -> str:
        return self.get_message()


class Training:
    """Workout basic class."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get mean speed."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Get the amount of calories lost.
           Separate calculation for every workout type"""
        pass

    def show_training_info(self) -> InfoMessage:
        """Returns info message about workout."""
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
        return self.duration * self.MIN_IN_HOUR


class Running(Training):
    """Workout: running."""
    COEF_CALOR_1: int = 18
    COEF_CALOR_2: int = 20

    def get_spent_calories(self) -> float:
        """Get amount of calories spent during running."""
        speed: float = super().get_mean_speed()
        duration_minutes = super().get_duration_minutes()
        spent_calor: float = ((self.COEF_CALOR_1 * speed - self.COEF_CALOR_2)
                              * self.weight / self.M_IN_KM * duration_minutes)
        return spent_calor


class SportsWalking(Training):
    """Workout: sport walking."""
    COEF_CALOR_1: float = 0.035
    COEF_CALOR_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Get amount of calories spent during sport walking"""
        speed: float = super().get_mean_speed()
        duration_minutes: float = super().get_duration_minutes()
        spent_calor: float = ((self.COEF_CALOR_1 * self.weight + (speed**2
                              // self.height) * self.COEF_CALOR_2
                              * self.weight) * duration_minutes)
        return spent_calor


class Swimming(Training):
    """Workout: swimming."""
    LEN_STEP: float = 1.38
    COEF_CALOR_1: float = 1.1
    COEF_CALOR_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Get mean speed of swimming"""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Get amount of calories spent during swimming"""
        speed: float = self.get_mean_speed()
        spent_calor: float = ((speed + self.COEF_CALOR_1)
                              * self.COEF_CALOR_2 * self.weight)
        return spent_calor


def read_package(workout_type: str, data: List) -> Training:
    """Read data received from sensors."""
    workouts: Dict[str, type] = ({'SWM': Swimming,
                                  'RUN': Running,
                                  'WLK': SportsWalking})
    return workouts[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
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
        try:
            training: Training = read_package(workout_type, data)
            main(training)
        except KeyError:
            print('Invalid workout type.')
