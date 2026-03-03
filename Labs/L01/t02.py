import math  # Імпортуємо вбудований модуль math для використання числа pi та функції квадратного кореня (sqrt)


# --- БАЗОВИЙ КЛАС ---
class Shape:  # Створюємо базовий клас Shape (Фігура), від якого будуть успадковуватися інші
    def get_area(self):  # Оголошуємо метод для обчислення площі
        pass  # Pass означає, що реалізація буде в класах-нащадках (це своєрідний шаблон)

    def get_perimeter(self):  # Оголошуємо метод для обчислення периметра
        pass  # Реалізація також буде у нащадках


# --- КЛАСИ КОНКРЕТНИХ ФІГУР ---
class Triangle(Shape):  # Клас Трикутник, успадковує Shape
    def __init__(self, a, b, c):  # Конструктор класу, приймає 3 сторони: a, b, c
        self.a = float(a)  # Зберігаємо сторону a, перетворюючи її на дробове число
        self.b = float(b)  # Зберігаємо сторону b
        self.c = float(c)  # Зберігаємо сторону c

    def get_perimeter(self):  # Метод обчислення периметра
        return self.a + self.b + self.c  # Периметр - це сума всіх трьох сторін

    def get_area(self):  # Метод обчислення площі
        p = self.get_perimeter() / 2  # Знаходимо півпериметр для формули Герона
        # Повертаємо площу за формулою Герона. math.sqrt - це квадратний корінь
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))


class Rectangle(Shape):  # Клас Прямокутник
    def __init__(self, a, b):  # Приймає 2 сторони
        self.a = float(a)  # Зберігаємо довжину
        self.b = float(b)  # Зберігаємо ширину

    def get_perimeter(self):  # Метод обчислення периметра
        return 2 * (self.a + self.b)  # Формула: 2 * (a + b)

    def get_area(self):  # Метод обчислення площі
        return self.a * self.b  # Формула: довжина * ширину


class Trapeze(Shape):  # Клас Трапеція
    def __init__(self, a, b, c, d):  # Приймає 4 параметри (2 основи, 2 бічні сторони)
        self.a = float(a)  # Зберігаємо першу основу
        self.b = float(b)  # Зберігаємо другу основу
        self.c = float(c)  # Зберігаємо першу бічну сторону
        self.d = float(d)  # Зберігаємо другу бічну сторону

    def get_perimeter(self):  # Периметр трапеції
        return self.a + self.b + self.c + self.d  # Сума всіх чотирьох сторін

    def get_area(self):  # Площа трапеції (складна формула за 4 сторонами)
        # Обчислюємо частину формули під коренем, щоб код був читабельним
        # Застосовуємо стандартну геометричну формулу площі трапеції через її сторони
        x = ((self.a - self.b) ** 2 + self.c ** 2 - self.d ** 2) / (2 * abs(self.a - self.b))
        height = math.sqrt(self.c ** 2 - x ** 2)  # Знаходимо висоту трапеції
        return ((self.a + self.b) / 2) * height  # Повертаємо площу (півсума основ на висоту)


class Parallelogram(Shape):  # Клас Паралелограм
    def __init__(self, a, b, h):  # Приймає 2 сторони і висоту
        self.a = float(a)  # Зберігаємо першу сторону (до якої проведена висота)
        self.b = float(b)  # Зберігаємо другу сторону
        self.h = float(h)  # Зберігаємо висоту

    def get_perimeter(self):  # Периметр паралелограма
        return 2 * (self.a + self.b)  # Сума сторін помножена на 2

    def get_area(self):  # Площа паралелограма
        return self.a * self.h  # Добуток сторони на висоту, проведену до неї


class Circle(Shape):  # Клас Круг
    def __init__(self, r):  # Приймає лише радіус
        self.r = float(r)  # Зберігаємо радіус

    def get_perimeter(self):  # Периметр (довжина кола)
        return 2 * math.pi * self.r  # Формула: 2 * pi * r

    def get_area(self):  # Площа круга
        return math.pi * (self.r ** 2)  # Формула: pi * r у квадраті


# --- ОСНОВНА ЛОГІКА ПРОГРАМИ ---

def process_shapes_from_file(filename):  # Створюємо функцію для обробки файлу
    # Словник, який співставляє текстові назви фігур з їхніми класами
    shape_classes = {
        "Triangle": Triangle,
        "Rectangle": Rectangle,
        "Trapeze": Trapeze,
        "Parallelogram": Parallelogram,
        "Circle": Circle
    }

    shapes_list = []  # Створюємо порожній список, де будемо зберігати створені об'єкти фігур

    try:  # Починаємо блок перевірки помилок (на випадок, якщо файлу немає)
        with open(filename, 'r', encoding='utf-8') as file:  # Відкриваємо файл для читання ('r')
            for line in file:  # Перебираємо файл рядок за рядком
                parts = line.split()  # Розбиваємо рядок на слова (за пробілами)
                if not parts:  # Якщо рядок порожній...
                    continue  # ...пропускаємо його і йдемо до наступного

                shape_name = parts[0]  # Перше слово - це назва фігури (напр., Triangle)
                params = parts[1:]  # Усі інші слова - це параметри (сторони, радіус тощо)

                if shape_name in shape_classes:  # Якщо така фігура є у нашому словнику...
                    shape_class = shape_classes[shape_name]  # ...дістаємо відповідний клас
                    # Створюємо об'єкт фігури, передаючи параметри за допомогою розпакування (*params)
                    shape_obj = shape_class(*params)
                    shapes_list.append((shape_name, shape_obj))  # Додаємо кортеж (назва, об'єкт) у список

    except FileNotFoundError:  # Якщо файл з такою назвою не знайдено
        print(f"Помилка: Файл {filename} не знайдено.")  # Виводимо повідомлення про помилку
        return  # Виходимо з функції

    # Перевіряємо, чи список фігур не порожній
    if not shapes_list:
        print("Файл порожній або не містить коректних даних.")
        return

    # --- ПОШУК МАКСИМУМІВ ---

    # Спочатку припускаємо, що перша фігура має найбільшу площу і периметр
    max_area_shape = shapes_list[0]
    max_perimeter_shape = shapes_list[0]

    # Перебираємо всі збережені фігури у списку
    for name, shape in shapes_list:
        # Якщо площа поточної фігури більша за збережену максимальну...
        if shape.get_area() > max_area_shape[1].get_area():
            max_area_shape = (name, shape)  # ...оновлюємо лідера за площею

        # Якщо периметр поточної фігури більший за збережений максимальний...
        if shape.get_perimeter() > max_perimeter_shape[1].get_perimeter():
            max_perimeter_shape = (name, shape)  # ...оновлюємо лідера за периметром

    # Виводимо результати на екран
    print(f"\n--- Аналіз файлу {filename} ---")
    print("Фігура з найбільшою площею:")
    # Виводимо назву і площу, округлену до 2 знаків після коми (.2f)
    print(f"- {max_area_shape[0]}, Площа: {max_area_shape[1].get_area():.2f}")

    print("Фігура з найбільшим периметром:")
    # Виводимо назву і периметр, округлений до 2 знаків після коми
    print(f"- {max_perimeter_shape[0]}, Периметр: {max_perimeter_shape[1].get_perimeter():.2f}")


# Запуск програми (точка входу)
if __name__ == "__main__":
    # Викликаємо функцію для файлу input01.txt (ви можете змінити назву під свої файли)
    process_shapes_from_file("input01.txt")
    # process_shapes_from_file("input02.txt")
    # process_shapes_from_file("input03.txt")