def gen_sum_d():
    # Ініціалізуємо базові значення a_1 та a_2 згідно з умовою
    a_prev2 = 0  # a_1
    a_prev1 = 1  # a_2

    # Лічильник k для відстеження індексу
    k = 1
    # Змінна для накопичення загальної суми
    current_sum = 0

    while True:
        if k == 1:
            # Для k=1 значення a_k вже відоме
            a_k = a_prev2
        elif k == 2:
            # Для k=2 значення a_k вже відоме
            a_k = a_prev1
        else:
            # Для k >= 3 обчислюємо a_k за рекурентною формулою
            a_k = a_prev1 + k * a_prev2
            # Оновлюємо попередні значення для наступних ітерацій
            a_prev2 = a_prev1
            a_prev1 = a_k

        # Обчислюємо черговий доданок: 2^k * a_k
        term = (2 ** k) * a_k
        # Додаємо його до загальної суми
        current_sum += term

        # Видаємо накопичену суму S_k
        yield current_sum
        k += 1


n_sum = 4
generator_d = gen_sum_d()

for _ in range(n_sum):
    result_d = next(generator_d)

print(f"Завдання d: S_{n_sum} = {result_d}")