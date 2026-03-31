import turtle
import random


# ==========================================
# ЧАСТИНА 1: БАЗОВИЙ КЛАС
# ==========================================

class Figure:
    """
    Базовий клас для всіх геометричних фігур.
    Реалізує загальну логіку позиціонування, кольору та переміщення.
    """

    def __init__(self, x, y, color="black"):
        self.x = x  # Координата X (базова точка фігури)
        self.y = y  # Координата Y (базова точка фігури)
        self.color = color  # Колір малювання
        self.is_visible = False  # Прапорець: чи намальована фігура зараз на екрані
        self.bg_color = "white"  # Колір фону екрану (для "стирання" фігури)

    def set_color(self, color):
        """Встановлює новий колір для фігури"""
        self.color = color

    def draw(self):
        """Зображує фігуру, якщо її ще немає на екрані"""
        if not self.is_visible:  # Перевіряємо, чи фігура вже не намальована
            turtle.color(self.color)  # Встановлюємо колір черепашки
            self._draw_shape()  # Викликаємо метод малювання конкретної форми (поліморфізм)
            self.is_visible = True  # Оновлюємо статус: фігура на екрані

    def erase(self):
        """Стирає фігуру, малюючи її кольором фону"""
        if self.is_visible:  # Стираємо лише якщо фігура намальована
            turtle.color(self.bg_color)  # Змінюємо колір на колір фону
            self._draw_shape()  # Малюємо фігуру поверх старої (ховаємо її)
            self.is_visible = False  # Оновлюємо статус: фігури немає на екрані

    def move(self, dx, dy):
        """Переміщує фігуру на задані зміщення dx та dy"""
        was_visible = self.is_visible  # Запам'ятовуємо, чи була фігура видимою
        if was_visible:
            self.erase()  # Якщо так, стираємо її зі старої позиції

        self.x += dx  # Змінюємо координату X
        self.y += dy  # Змінюємо координату Y

        if was_visible:
            self.draw()  # Малюємо на новій позиції, якщо вона була видимою раніше

    def _draw_shape(self):
        """
        Абстрактний метод. Логіка малювання специфічної форми.
        Повинен бути реалізований у кожному класі-нащадку.
        """
        pass  # Заглушка. Базовий клас не знає, яку форму малювати.


# ==========================================
# ЧАСТИНА 2: КЛАСИ-НАЩАДКИ (ФОРМИ)
# ==========================================

class Circle(Figure):
    def __init__(self, x, y, radius, color="black"):
        super().__init__(x, y, color)  # Виклик конструктора базового класу
        self.radius = radius  # Додаємо специфічне поле - радіус

    def _draw_shape(self):
        # Позиція для кола - це його центр. Але turtle.circle() малює від нижньої точки.
        # Тому ми опускаємо черепашку вниз на відстань радіуса перед малюванням.
        turtle.penup()
        turtle.goto(self.x, self.y - self.radius)
        turtle.pendown()

        turtle.begin_fill()  # Починаємо заливку
        turtle.circle(self.radius)  # Малюємо коло
        turtle.end_fill()  # Завершуємо заливку


class Triangle(Figure):
    # Рівносторонній трикутник. Позиція (x,y) - лівий нижній кут.
    def __init__(self, x, y, side, color="black"):
        super().__init__(x, y, color)
        self.side = side

    def _draw_shape(self):
        turtle.penup()
        turtle.goto(self.x, self.y)  # Йдемо в лівий нижній кут
        turtle.pendown()

        turtle.begin_fill()
        for _ in range(3):  # Цикл для 3-х сторін
            turtle.forward(self.side)  # Малюємо сторону
            turtle.left(120)  # Повертаємо на 120 градусів (зовнішній кут рівностороннього трикутника)
        turtle.end_fill()


class Rectangle(Figure):
    # Прямокутник. Позиція (x,y) - лівий нижній кут.
    def __init__(self, x, y, width, height, color="black"):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

    def _draw_shape(self):
        turtle.penup()
        turtle.goto(self.x, self.y)
        turtle.pendown()

        turtle.begin_fill()
        for _ in range(2):  # Малюємо 2 пари сторін
            turtle.forward(self.width)
            turtle.left(90)
            turtle.forward(self.height)
            turtle.left(90)
        turtle.end_fill()


class Square(Rectangle):
    # Квадрат успадковує Прямокутник.
    # Його ширина і висота однакові, тому в конструкторі ми приймаємо лише side.
    def __init__(self, x, y, side, color="black"):
        super().__init__(x, y, side, side, color)  # Передаємо side і як width, і як height у Rectangle


class Trapeze(Figure):
    # Рівнобічна трапеція. Позиція (x,y) - лівий нижній кут.
    def __init__(self, x, y, base_bottom, base_top, height, color="black"):
        super().__init__(x, y, color)
        self.base_bottom = base_bottom
        self.base_top = base_top
        self.height = height

    def _draw_shape(self):
        turtle.penup()
        turtle.goto(self.x, self.y)
        turtle.pendown()

        # Обчислюємо зміщення верхньої основи відносно нижньої (оскільки трапеція рівнобічна)
        offset = (self.base_bottom - self.base_top) / 2

        turtle.begin_fill()
        turtle.goto(self.x + self.base_bottom, self.y)  # Нижня основа
        turtle.goto(self.x + self.base_bottom - offset, self.y + self.height)  # Права бокова сторона
        turtle.goto(self.x + offset, self.y + self.height)  # Верхня основа
        turtle.goto(self.x, self.y)  # Ліва бокова сторона
        turtle.end_fill()


# ==========================================
# ЧАСТИНА 3: КОМПОЗИЦІЯ (КЛАС АВТОМОБІЛЬ)
# ==========================================

class Car:
    """
    Клас, що демонструє Композицію.
    Автомобіль складається з кількох фігур.
    """

    def __init__(self, x, y):
        # Ініціалізуємо складові частини автомобіля відносно його базової координати (x, y)
        self.body = Rectangle(x, y + 20, 120, 40, "blue")  # Корпус
        self.roof = Trapeze(x + 20, y + 60, 80, 40, 30, "lightblue")  # Дах з вікнами
        self.wheel_front = Circle(x + 90, y + 20, 15, "black")  # Переднє колесо
        self.wheel_back = Circle(x + 30, y + 20, 15, "black")  # Заднє колесо

        # Зберігаємо всі частини у список для зручності
        self.parts = [self.body, self.roof, self.wheel_front, self.wheel_back]

    def draw(self):
        """Зображує весь автомобіль, малюючи кожну його частину"""
        for part in self.parts:
            part.draw()

    def move(self, dx, dy):
        """Переміщує автомобіль, викликаючи move() для кожної його частини"""
        for part in self.parts:
            part.move(dx, dy)


# ==========================================
# ЧАСТИНА 4: ГОЛОВНА ПРОГРАМА (ВИКОНАННЯ)
# ==========================================

def main():
    # Налаштування екрану turtle
    screen = turtle.Screen()
    screen.title("ООП Графіка: Наслідування, Поліморфізм та Композиція")
    screen.setup(width=800, height=600)

    # Вимикаємо анімацію малювання для швидкості (важливо для 100 фігур)
    turtle.tracer(0)
    turtle.hideturtle()

    # 1. Створення та переміщення автомобіля
    print("Малюємо автомобіль...")
    my_car = Car(-300, 100)
    my_car.draw()
    turtle.update()  # Оновлюємо екран, бо tracer(0)

    # Анімація переміщення автомобіля (зміщуємо його 50 разів праворуч)
    import time
    for _ in range(50):
        my_car.move(5, 0)
        turtle.update()
        time.sleep(0.05)

    # 2. Малювання 100 випадкових фігур
    print("Малюємо 100 випадкових фігур...")
    colors = ["red", "green", "yellow", "purple", "orange", "cyan", "magenta"]

    for _ in range(100):
        shape_type = random.randint(1, 5)  # Випадково обираємо тип фігури
        x = random.randint(-350, 350)
        y = random.randint(-250, 250)
        color = random.choice(colors)

        if shape_type == 1:
            fig = Circle(x, y, random.randint(10, 40), color)
        elif shape_type == 2:
            fig = Triangle(x, y, random.randint(20, 60), color)
        elif shape_type == 3:
            fig = Rectangle(x, y, random.randint(30, 80), random.randint(20, 50), color)
        elif shape_type == 4:
            fig = Square(x, y, random.randint(20, 60), color)
        else:
            fig = Trapeze(x, y, random.randint(50, 80), random.randint(20, 40), random.randint(20, 50), color)

        fig.draw()

    turtle.update()  # Показуємо всі намальовані фігури
    print("Готово! Закрийте вікно, щоб вийти.")
    turtle.done()


if __name__ == "__main__":
    main()