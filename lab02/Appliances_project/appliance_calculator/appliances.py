import abc
from typing import Union

class Appliance(abc.ABC):
    """
    Абстрактный базовый класс для всех бытовых приборов.
    """
    def __init__(self, name: str, power_consumption_watts: Union[int, float]):
        if not isinstance(name, str) or not name:
            raise ValueError("Имя прибора должно быть непустой строкой.")
        if not isinstance(power_consumption_watts, (int, float)) or power_consumption_watts <= 0:
            raise ValueError("Потребление электроэнергии должно быть положительным числом.")

        self._name = name # managed - атрибут (приватный, но доступен через property)
        self._power_consumption_watts = power_consumption_watts
        self._is_on = False # Статус включен/выключен

    # managed-атрибуты
    @property
    def name(self) -> str:
        return self._name

    @property
    def power_consumption_watts(self) -> Union[int, float]:
        return self._power_consumption_watts

    @property
    def is_on(self) -> bool:
        return self._is_on

    # Декоратор
    @abc.abstractmethod
    def calculate_energy_consumption(self, hours: Union[int, float]) -> float:
        """
        Рассчитывает потребление электроэнергии в кВт*ч за заданное количество часов.
        Должен быть реализован в подклассах.
        """
        pass

    def turn_on(self):
        """Включает прибор."""
        self._is_on = True
        print(f"{self.name} включен.")

    def turn_off(self):
        """Выключает прибор."""
        self._is_on = False
        print(f"{self.name} выключен.")

    # dunder-методы
    def __str__(self) -> str:
        status = "включен" if self.is_on else "выключен"
        return f"{self.name} (Мощность: {self.power_consumption_watts} Вт, Статус: {status})"

    def __repr__(self) -> str:
        return f"Appliance(name='{self.name}', power_consumption_watts={self.power_consumption_watts})"

# Иерархия наследования
class Iron(Appliance):
    """
    Класс для утюга.
    """
    def __init__(self, name: str, power_consumption_watts: Union[int, float], steam_booster: bool = False):
        super().__init__(name, power_consumption_watts)
        if not isinstance(steam_booster, bool):
            raise ValueError("Параметр steam_booster должен быть булевым.")
        self._steam_booster = steam_booster # managed-атрибут

    @property
    def steam_booster(self) -> bool:
        return self._steam_booster

    # Декоратор @abc.abstractmethod (реализация)
    def calculate_energy_consumption(self, hours: Union[int, float]) -> float:
        """
        Рассчитывает потребление электроэнергии для утюга в кВт*ч.
        """
        if not self.is_on:
            return 0.0
        if not isinstance(hours, (int, float)) or hours < 0:
            raise ValueError("Время должно быть неотрицательным числом.")

        # Предполагаем, что мощность используется постоянно, пока включен.
        # В реальности мощность утюга меняется, но для упрощения моделируем так.
        # Если нужно учитывать режим "паровой удар", можно усложнить.
        consumption_kwh = (self.power_consumption_watts / 1000) * hours
        return consumption_kwh

    # dunder-методы
    def __str__(self) -> str:
        status = "включен" if self.is_on else "выключен"
        booster_status = "с паровым усилением" if self.steam_booster else "без парового усиления"
        return f"Утюг '{self.name}' (Мощность: {self.power_consumption_watts} Вт, {booster_status}, Статус: {status})"

    def __repr__(self) -> str:
        return f"Iron(name='{self.name}', power_consumption_watts={self.power_consumption_watts}, steam_booster={self.steam_booster})"

class TV(Appliance):
    """
    Класс для телевизора.
    """
    def __init__(self, name: str, power_consumption_watts: Union[int, float], screen_size_inches: Union[int, float]):
        super().__init__(name, power_consumption_watts)
        if not isinstance(screen_size_inches, (int, float)) or screen_size_inches <= 0:
            raise ValueError("Размер экрана должен быть положительным числом.")
        self._screen_size_inches = screen_size_inches # managed-атрибут

    @property
    def screen_size_inches(self) -> Union[int, float]:
        return self._screen_size_inches

    def calculate_energy_consumption(self, hours: Union[int, float]) -> float:
        """
        Рассчитывает потребление электроэнергии для телевизора в кВт*ч.
        """
        if not self.is_on:
            return 0.0
        if not isinstance(hours, (int, float)) or hours < 0:
            raise ValueError("Время должно быть неотрицательным числом.")

        consumption_kwh = (self.power_consumption_watts / 1000) * hours
        return consumption_kwh

    def __str__(self) -> str:
        status = "включен" if self.is_on else "выключен"
        return f"Телевизор '{self.name}' (Мощность: {self.power_consumption_watts} Вт, Диагональ: {self.screen_size_inches}\", Статус: {status})"

    def __repr__(self) -> str:
        return f"TV(name='{self.name}', power_consumption_watts={self.power_consumption_watts}, screen_size_inches={self.screen_size_inches})"

class WashingMachine(Appliance):
    """
    Класс для стиральной машины.
    """
    def __init__(self, name: str, power_consumption_watts: Union[int, float], capacity_kg: Union[int, float]):
        super().__init__(name, power_consumption_watts)
        if not isinstance(capacity_kg, (int, float)) or capacity_kg <= 0:
            raise ValueError("Загрузка должна быть положительным числом.")
        self._capacity_kg = capacity_kg # managed-атрибут

    @property
    def capacity_kg(self) -> Union[int, float]:
        return self._capacity_kg

    def calculate_energy_consumption(self, hours: Union[int, float]) -> float:
        """
        Рассчитывает потребление электроэнергии для стиральной машины в кВт*ч.
        Предполагается, что указанное время - это время работы цикла.
        """
        if not self.is_on:
            return 0.0
        if not isinstance(hours, (int, float)) or hours < 0:
            raise ValueError("Время должно быть неотрицательным числом.")

        consumption_kwh = (self.power_consumption_watts / 1000) * hours
        return consumption_kwh

    def __str__(self) -> str:
        status = "включена" if self.is_on else "выключена"
        return f"Стиральная машина '{self.name}' (Мощность: {self.power_consumption_watts} Вт, Загрузка: {self.capacity_kg} кг, Статус: {status})"

    def __repr__(self) -> str:
        return f"WashingMachine(name='{self.name}', power_consumption_watts={self.power_consumption_watts}, capacity_kg={self.capacity_kg})"
