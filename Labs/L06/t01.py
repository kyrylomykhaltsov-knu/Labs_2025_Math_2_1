class ProtectedDictIntIterator:
    def __init__(self, data_dict):
        # Отримуємо список ключів і сортуємо їх
        self._sorted_keys = sorted(data_dict.keys())
        self._current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < len(self._sorted_keys):
            key_to_return = self._sorted_keys[self._current_index]
            self._current_index += 1
            return key_to_return
        else:
            raise StopIteration


# ==========================================
# ГОЛОВНИЙ КЛАС СЛОВНИКА (Завдання 5.2.1)
# ==========================================

class ProtectedDictInt:
    """
    Клас, що поводиться як словник із додатковим захистом.
    Обмеження:
    - Ключами можуть бути лише цілі числа (int).
    - Змінювати значення для вже існуючого ключа заборонено.
    """

    def __init__(self):
        # Використовуємо композицію: зберігаємо стандартний словник Python
        # всередині нашого класу. Символ '_' (підкреслення) означає,
        # що цей атрибут призначений лише для внутрішнього використання.
        self._data = {}

    def __iter__(self):
         return ProtectedDictIntIterator(self._data)

    def _validate_key(self, key):
        """
        Допоміжний приватний метод для перевірки типу ключа.
        Генерує помилку TypeError, якщо ключ не є цілим числом.
        """
        if not isinstance(key, int):
            raise TypeError(f"Ключ має бути цілим числом, отримано {type(key).__name__}")

    # --- Перевантаження доступу за квадратними дужками [] ---

    def __setitem__(self, key, value):
        """
        Викликається при спробі записати значення: my_dict[key] = value
        Відповідає за додавання нової пари.
        """
        # 1. Перевіряємо, чи є ключ цілим числом
        self._validate_key(key)

        # 2. Перевіряємо, чи такий ключ вже існує, щоб заборонити зміну (перезапис)
        if key in self._data:
            raise ValueError(f"Ключ {key} вже існує. Зміна значень заборонена.")

        # 3. Якщо всі перевірки пройдені, додаємо нову пару до внутрішнього словника
        self._data[key] = value

    def __getitem__(self, key):
        """
        Викликається при спробі прочитати значення: result = my_dict[key]
        """
        # Повертаємо значення з нашого внутрішнього словника.
        return self._data[key]

    # --- Перевантаження математичних операторів (+, -) ---

    def __add__(self, other):
        """
        Викликається при використанні оператора '+': new_dict = my_dict + other
        Операція створює та повертає НОВИЙ словник, щоб не змінювати оригінальний.
        """
        new_dict = ProtectedDictInt()

        # Копіюємо всі існуючі дані з поточного словника в новий
        for k, v in self._data.items():
            new_dict._data[k] = v

        # Випадок 1: Правий операнд - це кортеж (ключ, значення)
        if isinstance(other, tuple) and len(other) == 2:
            key_to_add, val_to_add = other
            self._validate_key(key_to_add)

            # Перевіряємо на конфлікт ключів
            if key_to_add in new_dict._data:
                raise ValueError(f"Не вдалося додати кортеж: Ключ {key_to_add} вже існує.")
            new_dict._data[key_to_add] = val_to_add

        # Випадок 2: Правий операнд - це інший словник ProtectedDictInt
        elif isinstance(other, ProtectedDictInt):
            for key_to_add, val_to_add in other._data.items():
                if key_to_add in new_dict._data:
                    raise ValueError(f"Не вдалося об'єднати: Ключ {key_to_add} вже існує в цільовому словнику.")
                new_dict._data[key_to_add] = val_to_add

        else:
            raise TypeError(
                "Непідтримуваний тип для оператора +. Очікується кортеж з 2 елементів або ProtectedDictInt.")

        return new_dict

    def __sub__(self, key_to_remove):
        """
        Викликається при використанні оператора '-': new_dict = my_dict - key
        Повертає НОВИЙ словник без вказаного ключа.
        """
        new_dict = ProtectedDictInt()

        # Копіюємо всі елементи, ОКРІМ того, який треба видалити
        for k, v in self._data.items():
            if k != key_to_remove:
                new_dict._data[k] = v

        return new_dict

    # --- Перевантаження вбудованих функцій Python ---

    def __contains__(self, key):
        """
        Викликається оператором 'in': if key in my_dict:
        Перевіряє, чи входить заданий ключ до словника.
        """
        return key in self._data

    def __len__(self):
        """
        Викликається функцією len()
        Визначає кількість елементів у словнику.
        """
        return len(self._data)

    def __str__(self):
        """
        Викликається функцією str() або print()
        Перетворює словник у рядок.
        """
        return str(self._data)


# ==========================================
# ГОЛОВНА ПРОГРАМА (ВИКОНАННЯ ТА ТЕСТУВАННЯ)
# ==========================================

def main():
    print("--- Створення та заповнення словника (оператор []) ---")
    my_dict = ProtectedDictInt()
    my_dict[2] = "Два"
    my_dict[1] = "Один"
    my_dict[3] = "Три"
    print(f"Словник: {my_dict}")
    print(f"Кількість елементів (len): {len(my_dict)}")
    # ==================
    print("\n--- перевірка ітератора")
    print("\n--- відсортовані ключі:")
    print(my_dict)
    # for key in my_dict:
    #     print(f"ключ: {key}, значення: {my_dict[key]}")
    # ==================
    print("\n--- Перевірка захисту від зміни існуючого значення ---")
    try:
        my_dict[2] = "Нова двійка"
    except Exception as e:
        print(f"Помилка успішно перехоплена: {e}")

    print("\n--- Перевірка типу ключа ---")
    try:
        my_dict["ключ"] = "Значення"
    except Exception as e:
        print(f"Помилка успішно перехоплена: {e}")

    print("\n--- Перевірка оператора + (додавання кортежу) ---")
    my_dict = my_dict + (4, "Чотири")
    print(f"Словник після додавання (4, 'Чотири'): {my_dict}")

    print("\n--- Перевірка оператора + (додавання іншого словника) ---")
    dict_to_add = ProtectedDictInt()
    dict_to_add[5] = "П'ять"
    dict_to_add[6] = "Шість"
    my_dict = my_dict + dict_to_add
    print(f"Словник після об'єднання: {my_dict}")

    print("\n--- Перевірка оператора - (видалення за ключем) ---")
    my_dict = my_dict - 3
    print(f"Словник після видалення ключа '3': {my_dict}")

    print("\n--- Перевірка оператора in ---")
    if 5 in my_dict:
        print("Ключ 5 присутній у словнику.")
    if 10 not in my_dict:
        print("Ключ 10 відсутній у словнику.")
    print("\n--- перевірка ітератора")
    print("\n--- відсортовані ключі:")
    for key in my_dict:
        print(f"ключ: {key}, значення: {my_dict[key]}")

if __name__ == "__main__":
    main()


