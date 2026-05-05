def gen_taylor_sin(x):
    # Початковий член ряду t_1 (при n=1: x^1 / 1! = x)
    term = x
    # Початкова сума ряду дорівнює першому члену
    current_sin = term
    # Починаємо з n=2 для наступних обчислень
    n = 2

    # Спочатку повертаємо t_1
    yield current_sin, term

    while True:
        # Рекурентно обчислюємо наступний доданок:
        # множимо на -x^2 і ділимо на два наступні числа факторіала
        term = term * (-x ** 2) / ((2 * n - 2) * (2 * n - 1))
        # Додаємо обчислений член до суми
        current_sin += term
        # Видаємо кортеж: (поточна сума, поточний доданок)
        yield current_sin, term
        n += 1


# Вхідні дані: кут у радіанах та задана точність
x_angle = math.pi / 4  # Наприклад, 45 градусів
eps = 1e-6

generator_e = gen_taylor_sin(x_angle)

# Використовуємо цикл з умовою (поки доданок більший за епсілон)
while True:
    # Отримуємо суму та останній доданок
    calc_sin, last_term = next(generator_e)
    # Якщо модуль доданка менший або дорівнює точності, зупиняємо цикл
    if abs(last_term) <= eps:
        break

# Отримуємо еталонне значення з бібліотеки math для порівняння
math_sin = math.sin(x_angle)

print(f"Завдання e:")
print(f"Обчислене значення sin({x_angle:.4f}) = {calc_sin:.7f}")
print(f"Бібліотечне значення sin({x_angle:.4f}) = {math_sin:.7f}")
print(f"Різниця: {abs(calc_sin - math_sin):.2e}")