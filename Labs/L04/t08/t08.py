# Клас, що описує одного пасажира
class Passenger:
    # Конструктор класу ініціалізує дані про пасажира
    def __init__(self, name, departure_city, arrival_city):
        self.name = name
        self.departure_city = departure_city
        self.arrival_city = arrival_city

    # Метод для розрахунку вартості квитка
    # Приймає список маршрутів (кортежів) та ціну за 1 км
    def calculate_ticket_cost(self, routes, price_per_km):
        # Проходимося по кожному маршруту у нашому списку
        for city1, city2, distance in routes:
            # Важливий момент: маршрут працює в обидва боки!
            # Відстань Київ-Львів така сама, як Львів-Київ.
            if (self.departure_city == city1 and self.arrival_city == city2) or \
                    (self.departure_city == city2 and self.arrival_city == city1):
                # Якщо знайшли збіг, рахуємо вартість: відстань множимо на тариф
                return distance * price_per_km

        # Якщо цикл завершився, але маршрут не знайдено
        return -1


# Головна функція програми
def main():
    routes = []  # Порожній список для збереження маршрутів
    passengers = []  # Порожній список для збереження об'єктів-пасажирів
    price_per_km = 0.0

    # Читаємо дані з файлу
    # Блок try-except потрібен, щоб програма не "впала", якщо файлу немає
    try:
        # Відкриваємо файл для читання ('r') з підтримкою української мови (utf-8)
        with open('data.txt', 'r', encoding='utf-8') as file:

            # Читаємо перший рядок - це ціна за 1 км. Перетворюємо текст у дробове число
            price_per_km = float(file.readline().strip())

            # Читаємо маршрути доки не зустрінемо роздільник "---"
            for line in file:
                line = line.strip()  # Видаляємо зайві пробіли та символи переносу рядка
                if line == "---":
                    break  # Зупиняємо цикл, якщо дійшли до роздільника

                # Розбиваємо рядок по комі. Отримуємо список: ['Київ', ' Львів', ' 540']
                parts = line.split(',')
                # Очищаємо кожну частину від пробілів та зберігаємо у змінні
                city1 = parts[0].strip()
                city2 = parts[1].strip()
                distance = int(parts[2].strip())  # Відстань перетворюємо на ціле число

                # Додаємо КОРТЕЖ (city1, city2, distance) у список маршрутів
                routes.append((city1, city2, distance))

            # Читаємо решту файлу (це вже пасажири)
            for line in file:
                line = line.strip()
                if not line:  # Якщо рядок порожній, пропускаємо його
                    continue

                parts = line.split(',')
                name = parts[0].strip()
                dep_city = parts[1].strip()
                arr_city = parts[2].strip()

                # Створюємо об'єкт класу Passenger
                new_passenger = Passenger(name, dep_city, arr_city)
                # Додаємо об'єкт у список пасажирів
                passengers.append(new_passenger)

    except FileNotFoundError:
        print("Помилка: Файл 'data.txt' не знайдено. Створіть його у папці з програмою.")
        return  # Завершуємо роботу програми

    # Розрахунок та виведення результатів
    print(f"Тариф: {price_per_km} грн/км")
    print("-" * 40)

    # Перебираємо кожного пасажира зі списку
    for p in passengers:
        cost = p.calculate_ticket_cost(routes, price_per_km)

        if cost != -1:
            print(f"Пасажир {p.name} ({p.departure_city} -> {p.arrival_city}): До сплати {cost} грн.")
        else:
            print(f"Пасажир {p.name} ({p.departure_city} -> {p.arrival_city}): Помилка! Маршрут не знайдено.")


# Запуск програми
if __name__ == "__main__":
    main()