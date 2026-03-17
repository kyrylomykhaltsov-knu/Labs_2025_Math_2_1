import math


class Equation:
    """Клас для моделювання лінійного рівняння bx + c = 0"""

    def __init__(self, b, c):
        self.b = b
        self.c = c

    def solve(self):
        """Повертає кортеж коренів лінійного рівняння"""
        if self.b == 0:
            if self.c == 0:
                return ("inf",)  # Нескінченна кількість розв'язків (0 = 0)
            else:
                return ()  # Немає розв'язків (наприклад, 5 = 0)
        else:
            return (-self.c / self.b,)

    def show(self):
        print(f"{self.b}x + {self.c} = 0")


class QuadraticEquation(Equation):
    """Клас для моделювання квадратного рівняння ax^2 + bx + c = 0"""

    def __init__(self, a, b, c):
        super().__init__(b, c)  # Викликаємо конструктор базового класу для b та c
        self.a = a

    def solve(self):
        # Якщо a == 0, то рівняння стає лінійним!
        # Делегуємо розв'язання батьківському класу
        if self.a == 0:
            return super().solve()

        discriminant = self.b ** 2 - 4 * self.a * self.c

        if discriminant < 0:
            return ()
        elif discriminant == 0:
            return (-self.b / (2 * self.a),)
        else:
            root1 = (-self.b - math.sqrt(discriminant)) / (2 * self.a)
            root2 = (-self.b + math.sqrt(discriminant)) / (2 * self.a)
            return tuple(sorted((root1, root2)))

    def show(self):
        print(f"{self.a}x^2 + {self.b}x + {self.c} = 0")


class BiQuadraticEquation(QuadraticEquation):
    """Клас для моделювання біквадратного рівняння ax^4 + bx^2 + c = 0"""

    def __init__(self, a, b, c):
        # Наслідуємось від квадратного, бо математика ідентична для y = x^2
        super().__init__(a, b, c)

    def solve(self):
        # 1. Знаходимо корені квадратного рівняння (для y) за допомогою методу батька
        y_roots = super().solve()

        # Обробляємо випадок нескінченної кількості коренів
        if y_roots == ("inf",):
            return ("inf",)

        x_roots = set()  # Використовуємо множину, щоб уникнути дублювання коренів (наприклад, +0.0 і -0.0)

        # 2. Зворотна заміна: x = ±sqrt(y)
        for y in y_roots:
            if y > 0:
                x_roots.add(math.sqrt(y))
                x_roots.add(-math.sqrt(y))
            elif y == 0:
                x_roots.add(0.0)
            # Якщо y < 0, дійсних коренів x немає, просто ігноруємо

        return tuple(sorted(x_roots))

    def show(self):
        print(f"{self.a}x^4 + {self.b}x^2 + {self.c} = 0")


def process_equations(filename):
    equations_list = []

    # 1. Читання файлу та створення об'єктів
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Розбиваємо рядок на числа та ігноруємо порожні рядки
                coeffs = [float(x) for x in line.split()]
                if not coeffs:
                    continue

                # Фабрика об'єктів: визначаємо тип за кількістю коефіцієнтів
                if len(coeffs) == 2:
                    eq = Equation(coeffs[0], coeffs[1])
                elif len(coeffs) == 3:
                    eq = QuadraticEquation(coeffs[0], coeffs[1], coeffs[2])
                elif len(coeffs) == 5:
                    # Для біквадратного a*x^4 + 0*x^3 + b*x^2 + 0*x + c = 0
                    # Беремо лише потрібні коефіцієнти: індекси 0, 2, 4
                    eq = BiQuadraticEquation(coeffs[0], coeffs[2], coeffs[4])
                else:
                    print(f"Невідомий формат коефіцієнтів: {coeffs}")
                    continue

                equations_list.append(eq)
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено.")
        return

    # Словник для підрахунку кількості рівнянь за кількістю коренів
    root_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, "inf": 0}

    # Списки для додаткового завдання (рівняння з рівно 1 розв'язком)
    equations_with_one_root = []

    # 2. Аналіз розв'язків
    print(f"\n--- Аналіз файлу {filename} ---")
    for eq in equations_list:
        roots = eq.solve()

        if roots == ("inf",):
            root_counts["inf"] += 1
        else:
            num_roots = len(roots)
            if num_roots in root_counts:
                root_counts[num_roots] += 1

            # Збираємо рівняння з рівно одним коренем для пошуку min/max
            if num_roots == 1:
                equations_with_one_root.append((eq, roots[0]))

    # Виведення статистики
    print("Кількість рівнянь, що мають:")
    print(f"  не мають розв'язків: {root_counts[0]}")
    print(f"  один розв'язок:      {root_counts[1]}")
    print(f"  два розв'язки:       {root_counts[2]}")
    print(f"  три розв'язки:       {root_counts[3]}")
    print(f"  чотири розв'язки:    {root_counts[4]}")
    print(f"  нескінченно багато:  {root_counts['inf']}")

    # 3. Пошук рівнянь з найменшим та найбільшим розв'язком (серед тих, де корінь рівно один)
    if equations_with_one_root:
        # Шукаємо мінімум та максимум за значенням кореня (елемент з індексом 1 у кортежі)
        min_eq_tuple = min(equations_with_one_root, key=lambda item: item[1])
        max_eq_tuple = max(equations_with_one_root, key=lambda item: item[1])

        print("\nСеред рівнянь з рівно 1 розв'язком:")
        print("Рівняння з НАЙМЕНШИМ розв'язком:")
        min_eq_tuple[0].show()
        print(f"Корінь: {min_eq_tuple[1]}")

        print("Рівняння з НАЙБІЛЬШИМ розв'язком:")
        max_eq_tuple[0].show()
        print(f"Корінь: {max_eq_tuple[1]}")
    else:
        print("\nРівнянь з рівно одним розв'язком не знайдено.")

# Виклик функції для тестових файлів
process_equations('input01.txt')
# process_equations('input02.txt')
# process_equations('input03.txt')