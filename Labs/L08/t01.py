import math


# --- Завдання (a): Послідовність a_n = x^n / n! ---
def gen_poslidovnist_a(x, n):
    """Генерує елементи послідовності a_k = x^k / k! до n включно."""
    a_k = 1.0  # Початкове значення: a_0 = x^0 / 0! = 1
    yield a_k  # Повертаємо a_0

    for k in range(1, n + 1):
        # Рекурентний крок: наступний член через попередній
        # a_k = a_{k-1} * (x / k)
        a_k *= (x / k)
        yield a_k  # Повертаємо поточний елемент


# --- Завдання (b): Гармонічна сума S_n = 1 + 1/2 + ... + 1/n ---
def gen_garmonichna_suma(n):
    """Генерує часткові суми гармонічного ряду до n."""
    potochna_suma = 0.0
    for k in range(1, n + 1):
        potochna_suma += 1 / k  # Додаємо новий член ряду до суми
        yield potochna_suma  # Повертаємо накопичену суму


# --- Завдання (c): Визначник тридіагональної матриці D_n ---
def gen_vyznachnyk(n):
    """Генерує визначники порядку k від 1 до n через рекурентне співвідношення."""
    # Рекурентна формула: D_k = 5*D_{k-1} - 6*D_{k-2}
    # Базові значення:
    # D_0 вважаємо рівним 1 (одиниця для рекуренції)
    # D_1 = |5| = 5
    d_minus_2 = 1  # Це D_0
    d_minus_1 = 5  # Це D_1

    yield d_minus_1  # Повертаємо D_1

    if n >= 2:
        for k in range(2, n + 1):
            # Обчислюємо поточний визначник
            d_potochnyi = 5 * d_minus_1 - 6 * d_minus_2
            yield d_potochnyi
            # Оновлюємо значення для наступного кроку
            d_minus_2, d_minus_1 = d_minus_1, d_potochnyi


# --- Завдання (d): Добуток P_n з рекурентною послідовністю a_k ---
def gen_dobutok_p(n):
    """Генерує добуток P_k на основі рекурентної послідовності a_k."""
    # Початкові умови для a_k: a_0=1, a_1=1, a_2=3
    a_m3, a_m2, a_m1 = 1.0, 1.0, 3.0  # a_0, a_1, a_2
    p_k = 1.0  # Початкове значення добутку

    # Розраховуємо добуток для перших трьох елементів (k=0, 1, 2)
    p_k *= (a_m3 / 1)  # k=0: P_0 = a_0 / 3^0
    if n >= 0: yield p_k

    if n >= 1:
        p_k *= (a_m2 / 3)  # k=1: P_1 = P_0 * (a_1 / 3^1)
        yield p_k

    if n >= 2:
        p_k *= (a_m1 / 9)  # k=2: P_2 = P_1 * (a_2 / 3^2)
        yield p_k

    # Розрахунок для k >= 3
    for k in range(3, n + 1):
        # Формула: a_k = a_{k-3} + (a_{k-2} / 2^{k-1})
        a_k = a_m3 + (a_m2 / (2 ** (k - 1)))
        # Оновлюємо добуток: P_k = P_{k-1} * (a_k / 3^k)
        p_k *= (a_k / (3 ** k))
        yield p_k
        # Зсуваємо значення послідовності a: a_0, a_1, a_2 -> a_1, a_2, a_k
        a_m3, a_m2, a_m1 = a_m2, a_m1, a_k


# --- Завдання (e): Ряд Тейлора для e^x з точністю eps ---
def gen_taylor_exp(x, eps):
    """Обчислює e^x через ряд Тейлора, поки доданок не стане меншим за eps."""
    potochnyi_dodanyk = 1.0  # Перший член: x^0 / 0! = 1
    zagalna_suma = potochnyi_dodanyk
    k = 1

    # Повертаємо початкову суму та перший член
    yield zagalna_suma, potochnyi_dodanyk

    # Цикл працює, поки модуль доданка більший за задану похибку
    while abs(potochnyi_dodanyk) > eps:
        # Рекурентне отримання наступного доданка:
        potochnyi_dodanyk *= (x / k)
        zagalna_suma += potochnyi_dodanyk
        yield zagalna_suma, potochnyi_dodanyk
        k += 1


# --- Основний блок для демонстрації роботи програми ---
if __name__ == "__main__":
    print("--- Завдання (a): Послідовність a_n (x=2, n=5) ---")
    print(list(gen_poslidovnist_a(2, 5)))

    print("\n--- Завдання (b): Гармонічна сума S_n (n=5) ---")
    print(list(gen_garmonichna_suma(5)))

    print("\n--- Завдання (c): Визначник матриці D_n (n=5) ---")
    print(list(gen_vyznachnyk(5)))

    print("\n--- Завдання (d): Добуток P_n (n=5) ---")
    print(list(gen_dobutok_p(5)))

    print("\n--- Завдання (e): Ряд Тейлора для e^x ---")
    x_test = 1.0
    epsilon = 1e-7

    rezultat = 0
    for s, dodanyk in gen_taylor_exp(x_test, epsilon):
        rezultat = s

    print(f"Обчислено при x={x_test}: {rezultat}")
    print(f"Значення з math.exp:   {math.exp(x_test)}")
    print(f"Різниця:               {abs(rezultat - math.exp(x_test))}")