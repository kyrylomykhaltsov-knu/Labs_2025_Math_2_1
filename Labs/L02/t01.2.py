import turtle
import math
import time
from random import randint, choice


# === 1. ОПИС КЛАСУ ===
class Triangle:
    def __init__(self, x1, y1, x2, y2):
        self.position = (0, 0)
        self.vertex1 = (x1, y1)
        self.vertex2 = (x2, y2)
        self.color = "black"

        # Атрибути для анімацій
        self.rotation = 0.0
        self.scale = (1.0, 1.0)
        self.pivot = None

    def set_position(self, x, y):
        self.position = (x, y)

    def set_color(self, color):
        self.color = color

    def set_rotation(self, rotation):
        self.rotation = rotation

    def set_scale(self, scale_x, scale_y):
        self.scale = (scale_x, scale_y)

    def set_pivot(self, pivot_x, pivot_y):
        self.pivot = (pivot_x, pivot_y)

    def get_absolute_vertices(self):
        """Повертає реальні координати вершин"""
        x0, y0 = self.position
        x1, y1 = x0 + self.vertex1[0], y0 + self.vertex1[1]
        x2, y2 = x0 + self.vertex2[0], y0 + self.vertex2[1]
        return (x0, y0), (x1, y1), (x2, y2)

    def get_centroid(self):
        """Точка перетину медіан"""
        p0, p1, p2 = self.get_absolute_vertices()
        cx = (p0[0] + p1[0] + p2[0]) / 3
        cy = (p0[1] + p1[1] + p2[1]) / 3
        return cx, cy

    def get_incenter(self):
        """Точка перетину бісектрис"""
        p0, p1, p2 = self.get_absolute_vertices()
        # Обчислюємо довжини сторін через теорему Піфагора (працює на всіх версіях Python)
        a = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        b = math.sqrt((p0[0] - p2[0]) ** 2 + (p0[1] - p2[1]) ** 2)
        c = math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)
        P = a + b + c

        ix = (a * p0[0] + b * p1[0] + c * p2[0]) / P
        iy = (a * p0[1] + b * p1[1] + c * p2[1]) / P
        return ix, iy

    def _transform(self, x, y):
        """Внутрішня математика: розтяг і поворот"""
        # Беремо pivot, якщо він заданий, інакше - стартову точку
        px, py = self.pivot if self.pivot is not None else self.position

        tx = x - px
        ty = y - py

        tx *= self.scale[0]
        ty *= self.scale[1]

        rx = tx * math.cos(self.rotation) - ty * math.sin(self.rotation)
        ry = tx * math.sin(self.rotation) + ty * math.cos(self.rotation)

        return px + rx, py + ry

    def draw(self, t):
        """Малювання трикутника"""
        p0, p1, p2 = self.get_absolute_vertices()

        tp0 = self._transform(*p0)
        tp1 = self._transform(*p1)
        tp2 = self._transform(*p2)

        t.penup()
        t.goto(tp0)
        t.pendown()

        t.fillcolor(self.color)
        t.begin_fill()
        t.goto(tp1)
        t.goto(tp2)
        t.goto(tp0)
        t.end_fill()


# === 2. ОСНОВНА ПРОГРАМА ===

screen = turtle.Screen()
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
turtle.tracer(0)  # Вимикаємо "живе" малювання для плавності

colors_list = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta", "lime", "gold"]

# --- ЗАВДАННЯ 2.2.1 ---
print("Малюємо 100 випадкових трикутників...")
for _ in range(100):
    while True:
        rand_x1 = randint(-60, 60)
        rand_y1 = randint(-60, 60)
        rand_x2 = randint(-60, 60)
        rand_y2 = randint(-60, 60)
        if (rand_x1 * rand_y2) - (rand_x2 * rand_y1) != 0:
            break

    my_triangle = Triangle(rand_x1, rand_y1, rand_x2, rand_y2)
    my_triangle.set_position(randint(-350, 350), randint(-300, 300))
    my_triangle.set_color(choice(colors_list))
    my_triangle.draw(t)

turtle.update()
time.sleep(2)
t.clear()

# --- ПІДГОТОВКА ДО АНІМАЦІЙ ---
anim_tri = Triangle(120, 0, 60, 160)
anim_tri.set_position(0, 0)

# --- ЗАВДАННЯ 2.2.2 (Обертання) ---
print("Анімація 1: Обертання навколо стартової вершини")
anim_tri.set_color("cyan")
# Встановлюємо стартову вершину як точку опори
anim_tri.set_pivot(*anim_tri.position)
for angle in range(0, 360, 5):
    t.clear()
    anim_tri.set_rotation(math.radians(angle))
    anim_tri.draw(t)
    turtle.update()
    time.sleep(0.01)
anim_tri.set_rotation(0)

# --- ЗАВДАННЯ 2.2.2 (Розтягування) ---
print("Анімація 2: Розтягування відносно стартової вершини")
anim_tri.set_color("magenta")
for i in list(range(10, 20)) + list(range(20, 10, -1)):
    t.clear()
    scale_val = i / 10.0
    anim_tri.set_scale(scale_val, scale_val)
    anim_tri.draw(t)
    turtle.update()
    time.sleep(0.04)
anim_tri.set_scale(1.0, 1.0)

# --- ЗАВДАННЯ 2.2.3 (Обертання - Бісектриси) ---
print("Анімація 3: Обертання навколо точки перетину бісектрис")
anim_tri.set_color("gold")
incenter = anim_tri.get_incenter()
anim_tri.set_pivot(*incenter)
for angle in range(0, 360, 5):
    t.clear()
    anim_tri.set_rotation(math.radians(angle))
    anim_tri.draw(t)
    t.penup();
    t.goto(incenter);
    t.dot(8, "red")
    turtle.update()
    time.sleep(0.01)
anim_tri.set_rotation(0)

# --- ЗАВДАННЯ 2.2.3 (Розтягування - Медіани) ---
print("Анімація 4: Розтягування відносно точки перетину медіан")
anim_tri.set_color("lime")
centroid = anim_tri.get_centroid()
anim_tri.set_pivot(*centroid)
for i in list(range(10, 20)) + list(range(20, 10, -1)):
    t.clear()
    scale_val = i / 10.0
    anim_tri.set_scale(scale_val, scale_val)
    anim_tri.draw(t)
    t.penup();
    t.goto(centroid);
    t.dot(8, "blue")
    turtle.update()
    time.sleep(0.04)

print("Демонстрацію завершено. Клікніть на вікно, щоб закрити.")
screen.exitonclick()