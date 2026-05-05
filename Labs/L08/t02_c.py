def gen_determinant_c():
    # Задаємо базові випадки D_1 та D_2
    d_prev2 = 2  # Відповідає D_1
    d_prev1 = 1  # Відповідає D_2

    # Видаємо перший базовий випадок
    yield d_prev2
    # Видаємо другий базовий випадок
    yield d_prev1

    while True:
        # Обчислюємо D_n за рекурентною формулою
        d_curr = 2 * d_prev1 - 3 * d_prev2
        # Видаємо знайдене значення
        yield d_curr
        # Зсовуємо змінні для наступної ітерації: D_{n-2} стає D_{n-1}
        d_prev2 = d_prev1
        # D_{n-1} стає щойно обчисленим D_n
        d_prev1 = d_curr


n_det = 5  # Порядок визначника
generator_c = gen_determinant_c()

for _ in range(n_det):
    result_c = next(generator_c)

print(f"Завдання c: D_{n_det} = {result_c}")