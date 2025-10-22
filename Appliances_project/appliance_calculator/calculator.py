from typing import List, Dict, Union
from .appliances import Appliance # Импорт из текущего пакета

class EnergyCalculator:
    """
    Класс для расчета потребления электроэнергии и стоимости.
    """
    def __init__(self, appliances: List[Appliance], tariff_kwh: Union[int, float] = 0.15): # tariff_kwh - цена за 1 кВт*ч
        if not isinstance(appliances, list) or not all(isinstance(app, Appliance) for app in appliances):
            raise TypeError("Список должен содержать объекты, унаследованные от Appliance.")
        if not isinstance(tariff_kwh, (int, float)) or tariff_kwh < 0:
            raise ValueError("Тариф за кВт*ч должен быть неотрицательным числом.")

        self.appliances = appliances
        self._tariff_kwh = tariff_kwh # managed-атрибут

    @property
    def tariff_kwh(self) -> Union[int, float]:
        return self._tariff_kwh

    @tariff_kwh.setter
    def tariff_kwh(self, value: Union[int, float]):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Тариф за кВт*ч должен быть неотрицательным числом.")
        self._tariff_kwh = value

    # 2 dunder-метода
    def __len__(self) -> int:
        return len(self.appliances)

    def __str__(self) -> str:
        appliance_list = "\n - ".join([str(app) for app in self.appliances])
        return f"Калькулятор энергии:\n" \
               f" Тариф за кВт*ч: {self.tariff_kwh}\n" \
               f" Количество приборов: {len(self)}\n" \
               f" Приборы:\n - {appliance_list}"

    def calculate_total_consumption_and_cost(self, period_hours: Union[int, float]) -> Dict[str, Union[float, List[Dict[str, Union[str, float]]]]]:
        """
        Рассчитывает общее потребление электроэнергии и стоимость за заданный период.
        Возвращает словарь с общими суммами и детализацией по каждому прибору.
        """
        if not isinstance(period_hours, (int, float)) or period_hours < 0:
            raise ValueError("Период в часах должен быть неотрицательным числом.")

        total_consumption_kwh = 0.0
        total_cost = 0.0
        detailed_results = []

        for appliance in self.appliances:
            if appliance.is_on:
                consumption_kwh = appliance.calculate_energy_consumption(period_hours)
                cost = consumption_kwh * self.tariff_kwh
                total_consumption_kwh += consumption_kwh
                total_cost += cost
                detailed_results.append({
                    "name": appliance.name,
                    "consumption_kwh": round(consumption_kwh, 3),
                    "cost": round(cost, 2)
                })
            else:
                detailed_results.append({
                    "name": appliance.name,
                    "consumption_kwh": 0.0,
                    "cost": 0.0
                })

        return {
            "total_consumption_kwh": round(total_consumption_kwh, 3),
            "total_cost": round(total_cost, 2),
            "details": detailed_results
        }
