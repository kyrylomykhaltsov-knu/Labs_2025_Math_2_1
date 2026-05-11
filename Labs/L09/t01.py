from abc import ABC, abstractmethod
import time


# --- АБСТРАКТНІ КЛАСИ (Без змін) ---

class MilitaryObject(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Spy(ABC):
    @abstractmethod
    def visit_general_staff(self, general_staff):
        pass

    @abstractmethod
    def visit_military_base(self, military_base):
        pass


# --- КОНКРЕТНІ ОБ'ЄКТИ ---

class GeneralStaff(MilitaryObject):
    def __init__(self, generals, secretPaper):
        self.generals = generals
        self.secretPaper = secretPaper

    def accept(self, visitor):
        # Пояснюємо студентам механіку Double Dispatch
        print(f"\n[LOG] Об'єкт GeneralStaff викликає visitor.{visitor.__class__.__name__}")
        visitor.visit_general_staff(self)

    def __str__(self):
        return f"🏢 ГЕНШТАБ: Генералів: {self.generals}, Секретних паперів: {self.secretPaper}"


class MilitaryBase(MilitaryObject):
    def __init__(self, officers, soldiers, jeeps, tanks):
        self.officers = officers
        self.soldiers = soldiers
        self.jeeps = jeeps
        self.tanks = tanks

    def accept(self, visitor):
        print(f"\n[LOG] Об'єкт MilitaryBase викликає visitor.{visitor.__class__.__name__}")
        visitor.visit_military_base(self)

    def __str__(self):
        return f"🎖️ БАЗА: Офіцерів: {self.officers}, Солдатів: {self.soldiers}, Техніки: {self.jeeps + self.tanks} од."


# --- КОНКРЕТНІ ВІДВІДУВАЧІ ---

class SecretAgent(Spy):
    def visit_general_staff(self, gs):
        print("🕵️ Агент непомітно сканує документи...")
        stolen = gs.secretPaper // 2
        gs.secretPaper -= stolen
        print(f"Результат: Викрадено {stolen} паперів. Штаб навіть не помітив.")

    def visit_military_base(self, mb):
        print(f"🕵️ Агент рахує техніку на базі: знайдено {mb.tanks} танків.")


class Saboteur(Spy):
    def visit_general_staff(self, gs):
        print("🧨 Диверсант заклав вибухівку в архіві!")
        gs.generals = max(0, gs.generals - 5)
        gs.secretPaper = 0
        print("Результат: Папери знищено, частина генералів нейтралізована.")

    def visit_military_base(self, mb):
        print("🧨 Диверсант мінує автопарк!")
        mb.jeeps = 0
        mb.tanks = 0
        mb.soldiers //= 2
        print("Результат: Вся техніка знищена, паніка серед особового складу.")


# --- ІНТЕРФЕЙС КОРИСТУВАЧА ---

def start_simulation():
    # Ініціалізація об'єктів
    staff = GeneralStaff(20, 100)
    base = MilitaryBase(10, 1000, 50, 10)

    print("=" * 50)
    print("  СИМУЛЯТОР ШПИГУНСЬКИХ ОПЕРАЦІЙ (Visitor Pattern)")
    print("=" * 50)

    while True:
        print(f"\nПОТОЧНИЙ СТАН:")
        print(staff)
        print(base)
        print("-" * 30)

        print("Оберіть ціль:")
        print("1. Відправити шпигуна в Генштаб")
        print("2. Відправити шпигуна на Військову базу")
        print("3. Завершити пару")

        target_choice = input("Ваш вибір (1-3): ")

        if target_choice == '3':
            print("\nСимуляція завершена. Студенти вільні!")
            break

        target = staff if target_choice == '1' else base

        print("\nОберіть тип шпигуна:")
        print("1. Секретний агент (тихий збір даних)")
        print("2. Диверсант (руйнування)")

        spy_choice = input("Ваш вибір (1-2): ")
        spy = SecretAgent() if spy_choice == '1' else Saboteur()

        print("\nВиконується операція...")
        time.sleep(1)  # Для ефекту очікування

        # КЛЮЧОВИЙ МОМЕНТ ПАТЕРНА:
        target.accept(spy)

        print("\n" + "-" * 30)
        input("Натисніть Enter, щоб продовжити...")


if __name__ == '__main__':
    start_simulation()