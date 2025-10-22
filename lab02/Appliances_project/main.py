import sys
import os
import datetime
from typing import List, Union

# Добавляем путь к пакету, чтобы его можно было импортировать
sys.path.append(os.path.join(os.path.dirname(__file__), 'appliance_calculator'))

from appliance_calculator.appliances import Appliance, Iron, TV, WashingMachine
from appliance_calculator.calculator import EnergyCalculator
from appliance_calculator.reporting import DocReport, XlsReport
from appliance_calculator.database import DatabaseManager

def get_user_input():
    """
    Получает от пользователя параметры для расчёта.
    """
    print("\n--- Ввод параметров ---")
    try:
        tariff = float(input("Введите тариф на электроэнергию (например, 0.15): "))
        period_hours = float(input("Введите период использования в часах (например, 24): "))

        # Создаем список приборов
        appliances_list: List[Appliance] = []

        # Утюг
        power_iron = float(input("Мощность утюга (Вт, например, 2000): "))
        steam_booster = input("Утюг с паровым усилением? (да/нет): ").lower() == 'да'
        appliances_list.append(Iron("Утюг", power_iron, steam_booster))

        # Телевизор
        power_tv = float(input("Мощность телевизора (Вт, например, 150): "))
        screen_tv = float(input("Диагональ телевизора (дюймы, например, 55): "))
        appliances_list.append(TV("Телевизор", power_tv, screen_tv))

        # Стиральная машина
        power_washer = float(input("Мощность стиральной машины (Вт, например, 2200): "))
        capacity_washer = float(input("Загрузка стиральной машины (кг, например, 7): "))
        appliances_list.append(WashingMachine("Стиральная машина", power_washer, capacity_washer))

        # Установка начального статуса "включено" для всех приборов (для примера)
        for app in appliances_list:
            app.turn_on()

        return tariff, period_hours, appliances_list

    except ValueError as e:
        print(f"Ошибка ввода: {e}. Пожалуйста, введите корректные числовые значения.")
        return None, None, None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при вводе: {e}")
        return None, None, None

def display_results(results: dict[str, Union[float, List[dict[str, Union[str, float]]]]]):
    """
    Отображает результаты расчёта.
    """
    print("\n--- Результаты расчёта ---")
    print(f"Общее потребление: {results['total_consumption_kwh']} кВт*ч")
    print(f"Общая стоимость: {results['total_cost']} $.")
    print("\nДетализация по приборам:")
    for item in results['details']:
        print(f"- {item['name']}: {item['consumption_kwh']} кВт*ч, {item['cost']} $.")

def main():
    """
    Основная функция программы.
    """
    print("Добро пожаловать в калькулятор энергопотребления бытовой техники!")

    # Инициализация менеджера БД
    db_manager = None
    try:
        db_manager = DatabaseManager()
        print(f"\nБаза данных {db_manager.db_name} готова.")
    except Exception as e:
        print(f"Не удалось инициализировать базу данных: {e}. Функционал сохранения в БД будет недоступен.")

    # Получаем данные от пользователя
    tariff, period_hours, appliance_objects = get_user_input()

    if tariff is None or period_hours is None or not appliance_objects:
        print("Не удалось получить корректные входные данные. Программа завершена.")
        return

    # Создаем калькулятор
    calculator = EnergyCalculator(appliances=appliance_objects, tariff_kwh=tariff)
    print(f"\nНастроен калькулятор:\n{calculator}")

    # Выполняем расчеты
    try:
        calculation_results = calculator.calculate_total_consumption_and_cost(period_hours=period_hours)
        display_results(calculation_results)

        # Сохранение результатов в БД, если менеджер БД инициализирован
        if db_manager:
            for detail in calculation_results['details']:
                # Ищем соответствующий объект прибора, чтобы получить его мощность
                appliance_obj = next((app for app in appliance_objects if app.name == detail['name']), None)
                if appliance_obj:
                    try:
                        db_manager.save_record(
                            appliance_name=detail['name'],
                            power_consumption_watts=appliance_obj.power_consumption_watts,
                            hours_used=period_hours,
                            consumption_kwh=detail['consumption_kwh'],
                            cost=detail['cost'],
                            tariff=calculator.tariff_kwh
                        )
                    except Exception as e:
                        print(f"Не удалось сохранить запись для {detail['name']} в БД: {e}")
                else:
                    print(f"Предупреждение: не найден объект для сохранения записи о {detail['name']} в БД.")

            # Отобразим последние записи из БД
            print("\n--- Последние записи из базы данных ---")
            all_records = db_manager.get_all_records()
            if all_records:
                for record in all_records[:5]: # Показываем последние 5
                    print(f"- {record['timestamp']} | {record['appliance_name']} | {record['consumption_kwh']} кВт*ч | {record['cost']} $.")
            else:
                print("В базе данных пока нет записей.")


        # Сохранение в файлы
        report_base_name = f"energy_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Сохранение в DOC
        doc_reporter = DocReport(report_base_name)
        doc_reporter.save_report(calculation_results)

        # Сохранение в XLS
        xls_reporter = XlsReport(report_base_name)
        xls_reporter.save_report(calculation_results)

    except ValueError as e:
        print(f"Ошибка расчёта: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка во время расчёта или сохранения: {e}")
    finally:
        # Закрываем соединение с БД
        if db_manager:
            db_manager.close()

if __name__ == "__main__":
    # Проверка наличия обязательных библиотек перед запуском
    try:
        import docx
        import openpyxl
        import pytest
    except ImportError as e:
        print(f"Ошибка: Необходимая библиотека не установлена: {e}")
        sys.exit(1)

    main()
