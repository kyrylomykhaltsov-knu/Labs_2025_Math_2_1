import math


class QuadraticEquation:
    def __init__(self, a=0.0, b=0.0, c=0.0):
        """
        Конструктор класу.
        Одночасно слугує 'конструктором копіювання', якщо передати об'єкт цього ж класу.
        """
        if isinstance(a, QuadraticEquation):
            # Реалізація конструктора копіювання
            self.a = a.a
            self.b = a.b
            self.c = a.c
        else:
            # Звичайна ініціалізація
            self.a = float(a)
            self.b = float(b)
            self.c = float(c)

    def solve(self):
        """
        Повертає розв'язки рівняння.
        Формат повернення:
        - () : порожній кортеж (немає розв'язків)
        - (x,) : кортеж з 1 елементом (один розв'язок)
        - (x1, x2) : кортеж з 2 елементами (два розв'язки)
        - float('inf') : нескінченна кількість розв'язків
        """
        # Випадок 1: a = 0 (рівняння не квадратне, а лінійне: bx + c = 0)
        if self.a == 0:
            if self.b == 0:
                if self.c == 0:
                    return float('inf')  # 0 = 0 (будь-яке x є розв'язком)
                else:
                    return ()  # c = 0, де c != 0 (немає розв'язків, напр. 5 = 0)
            else:
                return (-self.c / self.b,)  # Одне рішення лінійного рівняння

        # Випадок 2: a != 0 (класичне квадратне рівняння)
        discriminant = self.b ** 2 - 4 * self.a * self.c

        if discriminant > 0:
            x1 = (-self.b + math.sqrt(discriminant)) / (2 * self.a)
            x2 = (-self.b - math.sqrt(discriminant)) / (2 * self.a)
            return (x1, x2)
        elif discriminant == 0:
            x = -self.b / (2 * self.a)
            return (x,)
        else:
            return ()  # Дискримінант від'ємний, дійсних коренів немає

    def show(self):
        """
        Виводить рівняння у зручному вигляді на екран.
        """
        # Простий і хитрий спосіб вивести рівняння гарно, замінивши "+ -" на "-"
        eq_str = f"{self.a}x^2 + {self.b}x + {self.c} = 0"
        eq_str = eq_str.replace("+ -", "- ")
        print(eq_str)


def process_equations(filename):
    equations = []

    # 1. Зчитування даних з файлу
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 3:
                    # Створюємо об'єкт і додаємо в список
                    eq = QuadraticEquation(parts[0], parts[1], parts[2])
                    equations.append(eq)
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
        return

    # 2. Групування рівнянь за кількістю розв'язків
    no_solutions = []
    one_solution = []  # Будемо зберігати кортежі: (рівняння, корінь)
    two_solutions = []
    inf_solutions = []

    for eq in equations:
        roots = eq.solve()
        if roots == float('inf'):
            inf_solutions.append(eq)
        elif len(roots) == 0:
            no_solutions.append(eq)
        elif len(roots) == 1:
            one_solution.append((eq, roots[0]))
        elif len(roots) == 2:
            two_solutions.append(eq)

    # 3. Виведення результатів за групами
    print(f"\--- Аналіз файлу {filename} ---")

    print("\n[Не мають розв'язків]:")
    for eq in no_solutions: eq.show()

    print("\n[Мають один розв'язок]:")
    for eq, root in one_solution:
        eq.show()
        print(f"  -> x = {root:.4f}")

    print("\n[Мають два розв'язки]:")
    for eq in two_solutions: eq.show()

    print("\n[Мають нескінченну кількість розв'язків]:")
    for eq in inf_solutions: eq.show()

    # 4. Пошук найменшого та найбільшого розв'язку серед тих, що мають один корінь
    if one_solution:
        # Використовуємо lambda функцію, щоб порівнювати саме корінь (індекс 1 у кортежі)
        min_eq_tuple = min(one_solution, key=lambda item: item[1])
        max_eq_tuple = max(one_solution, key=lambda item: item[1])

        print("\n*** Додаткове завдання для рівнянь з 1 розв'язком ***")
        print("Рівняння з НАЙМЕНШИМ розв'язком:")
        min_eq_tuple[0].show()
        print(f" (Розв'язок: {min_eq_tuple[1]:.4f})")

        print("Рівняння з НАЙБІЛЬШИМ розв'язком:")
        max_eq_tuple[0].show()
        print(f" (Розв'язок: {max_eq_tuple[1]:.4f})")
    else:
        print("\n*** Рівнянь з рівно одним розв'язком не знайдено ***")
    print("-" * 40 + "\n")


# Демонстрація (передбачається, що файл input01.txt існує в тій же папці)
process_equations("input01.txt")

# Демонстрація конструктора копіювання для студентів:
eq1 = QuadraticEquation(1, -5, 6)
eq2 = QuadraticEquation(eq1)  # Спрацює конструктор копіювання
# eq1.show()
# eq2.show()