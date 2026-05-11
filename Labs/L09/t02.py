from abc import ABC, abstractmethod


# --- ІНТЕРФЕЙС СПОСТЕРІГАЧА ---

class Observer(ABC):
    @abstractmethod
    def onReceive(self, line):
        """Метод, який викликається, коли зчитується новий рядок"""
        pass


# --- СУБ'ЄКТ (FILE READER) ---

class FileReader:
    def __init__(self):
        self._observers = []  # Список підписників

    def attach(self, observer):
        """Додати нового спостерігача"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Видалити спостерігача"""
        self._observers.remove(observer)

    def notify(self, line):
        """Сповістити всіх підписників про новий рядок"""
        for observer in self._observers:
            observer.onReceive(line)

    def read_file(self, lines_list):
        """Імітація порядкового зчитування (замість реального файлу для тесту)"""
        print(f"\n🚀 Починаємо читання...")
        for line in lines_list:
            print(f"[FileReader] Прочитано: '{line}'")
            self.notify(line)  # Розсилаємо рядок усім підписникам


# --- КОНКРЕТНІ СПОСТЕРІГАЧІ ---

class ConsolePrinter(Observer):
    """Задача 1: Виводить рядки на екран"""

    def onReceive(self, line):
        print(f"   📢 [Printer] Відображаю: {line.strip()}")


class WordCounter(Observer):
    """Задача 2: Підраховує кількість слів"""

    def __init__(self):
        self.total_words = 0

    def onReceive(self, line):
        words = line.split()
        self.total_words += len(words)
        print(f"   📊 [Counter] Слів у цьому рядку: {len(words)} (Всього: {self.total_words})")


class WordFinder(Observer):
    """Задача 3: Шукає задане слово"""

    def __init__(self, target_word):
        self.target_word = target_word
        self.found = False

    def onReceive(self, line):
        if self.target_word.lower() in line.lower():
            self.found = True
            print(f"   🎯 [Finder] ЗНАЙДЕНО слово '{self.target_word}'!")


# --- ІНТЕРАКТИВНА ДЕМОНСТРАЦІЯ ---

def demo():
    reader = FileReader()

    # Текст для імітації файлу
    mock_file = [
        "Python is an amazing language",
        "The Observer pattern is useful",
        "Keep coding and learning",
        "Goodbye world"
    ]

    print("=== ТЕСТ ПАТЕРНА OBSERVER ===")

    # Створюємо спостерігачів
    printer = ConsolePrinter()
    counter = WordCounter()
    finder = WordFinder("pattern")

    # Сценарій взаємодії
    print("\nКрок 1: Підписуємо тільки Printer та Counter")
    reader.attach(printer)
    reader.attach(counter)
    reader.read_file(mock_file[:1])  # Читаємо лише перший рядок

    print("\nКрок 2: Додаємо Finder (шукаємо 'pattern')")
    reader.attach(finder)
    reader.read_file(mock_file[1:2])  # Читаємо другий рядок

    print("\nКрок 3: Відписуємо Printer (залишаємо тільки логіку)")
    reader.detach(printer)
    reader.read_file(mock_file[2:])  # Дочитуємо решту

    print(f"\n✅ ПІДСУМОК: Всього нараховано слів: {counter.total_words}")


if __name__ == "__main__":
    demo()