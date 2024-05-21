import json
import random
from datetime import datetime, timedelta

# Примерные координаты (широта, долгота) для каждой остановки
stops = {
    "7-й микрорайон": (52.29778, 104.29639),
    "Ярославского (по требованию)": (52.30000, 104.30000),
    "Баумана": (52.30222, 104.30417),
    "Подстанция": (52.30500, 104.30833),
    "Кинотехникум": (52.30750, 104.31250),
    "Пионерская": (52.31000, 104.31667),
    "Кинотеатр Восток": (52.31250, 104.32083),
    "Школьная": (52.31500, 104.32500),
    "Роща": (52.31750, 104.32917),
    "Норильская": (52.32000, 104.33333),
    "Узловая": (52.32250, 104.33750),
    "Трактовая": (52.32500, 104.34167),
    "Бакалея": (52.32750, 104.34583),
    "ДОК": (52.33000, 104.35000),
    "Иркутный мост": (52.33250, 104.35417),
    "Курорт Ангара": (52.33500, 104.35833),
    "2-я Железнодорожная": (52.33750, 104.36250),
    "Чайка": (52.34000, 104.36667),
    "Шмидта": (52.34250, 104.37083),
    "Жуковского": (52.34500, 104.37500),
    "Технический университет": (52.34750, 104.37917),
    "Институт МВД": (52.35000, 104.38333),
    "Академическая": (52.35250, 104.38750),
    "Университетский микрорайон": (52.35500, 104.39167),
    "Школа №55": (52.35750, 104.39583),
    "Ботанический Сад": (52.36000, 104.40000),
    "Вампилова": (52.36250, 104.40417),
    "Первомайский микрорайон": (52.36500, 104.40833)
}

def interpolate_coords(start, end, fraction):
    return (
        start[0] + (end[0] - start[0]) * fraction,
        start[1] + (end[1] - start[1]) * fraction
    )

def simulate_bus_route(stops, start_time, duration_minutes):
    data = []
    current_time = start_time
    total_distance = 0
    prev_stop_coords = None

    # Время в секундах между остановками
    time_between_stops = duration_minutes * 60 / (len(stops) - 1)

    stop_names = list(stops.keys())

    for i in range(len(stop_names) - 1):
        stop_name = stop_names[i]
        next_stop_name = stop_names[i + 1]
        prev_stop_coords = stops[stop_name]
        next_stop_coords = stops[next_stop_name]

        # Общее количество промежуточных точек между остановками
        num_intermediate_points = int(time_between_stops / 5)
        
        for j in range(num_intermediate_points):
            fraction = j / num_intermediate_points
            coords = interpolate_coords(prev_stop_coords, next_stop_coords, fraction)

            # Симуляция средней скорости (км/ч)
            speed = random.uniform(20, 40)

            # Добавление записи в массив данных
            data.append({
                "time": current_time.isoformat(),
                "stop": stop_name,
                "next_stop": next_stop_name,
                "latitude": coords[0],
                "longitude": coords[1],
                "speed_kmh": speed
            })

            current_time += timedelta(seconds=5)

        # Добавляем конечную точку текущего сегмента (следующая остановка)
        data.append({
            "time": current_time.isoformat(),
            "stop": stop_name,
            "next_stop": next_stop_name,
            "latitude": next_stop_coords[0],
            "longitude": next_stop_coords[1],
            "speed_kmh": random.uniform(20, 40)
        })
        
        current_time += timedelta(seconds=5)

    return data

# Начало маршрута
start_time = datetime(2024, 5, 21, 12, 0, 0)
duration_minutes = 70

# Симуляция данных для маршрута
route_data = simulate_bus_route(stops, start_time, duration_minutes)

# Запись данных в JSON
with open('bus_route.json', 'w', encoding='utf-8') as f:
    json.dump(route_data, f, ensure_ascii=False, indent=4)

print("JSON файл с данными о маршруте создан: bus_route.json")