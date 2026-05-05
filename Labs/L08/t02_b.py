import math


def gen_product_b():
    # Початкове значення добутку P_0 (нейтральний елемент для множення)
    current_p = 1
    # Лічильник i починаємо з 1 згідно з умовою (i=1..n)
    i = 1

    while True:
        # Обчислюємо черговий множник: 1 / (i + 1!)
        # math.factorial(1) тут для строгої відповідності формулі
        term = 1 / (i + math.factorial(1))
        # Оновлюємо значення добутку
        current_p *= term
        # Повертаємо поточне значення добутку P_i
        yield current_p
        # Переходимо до наступного індексу
        i += 1


# Задане значення n
n_target = 4
generator_b = gen_product_b()

# Проходимо n кроків циклу для отримання потрібного добутку
for _ in range(n_target):
    result_b = next(generator_b)

print(f"Завдання b: P_{n_target} = {result_b}")