import os

class CatInfoMgr():
    """Общая информацию о каталоге игр"""

    def __init__(self):
        """Инициализация класса

        :return: Функция не возвращает результат
        """

        # Общая информация о каталоге игр
        self.__info = ""

        # Путь к файлу с информацией
        self.__filepath = ""

        # Текст последней ошибки
        self.__err_msg = ""


    def get_last_error(self):
        """Получить текст последней ошибки

        :return: Текст последней ошибки
        """

        return self.__err_msg


    def get_file_path(self):
        """Получить путь к используемому файлу

        :return: Путь к файлу
        """

        return self.__filepath


    def set_file_path(self, filepath):
        """Задать путь к используемому файлу

        :param filepath: Путь к XML файлу
        :return: Функция не возвращает результат
        """

        self.__filepath = str(filepath).strip()


    def get_info(self):
        """Получить информацию о каталоге

        :return: Строка с информацией
        """

        return self.__info

    def set_info(self, info_str):
        """Задать информацию о каталоге

        :param info_str: Текст с информацией для пользователя
        :return: Функция не возвращает результат
        """

        self.__info = str(info_str).strip()


    def load_info_from_file(self):
        """Загрузить информацию о каталоге из файла

        :return: True, в случае успеха
        """

        if not os.path.exists(self.__filepath):
            self.__err_msg = f"Файл {self.__filepath} не существует"
            return False

        with open(self.__filepath, encoding="utf-8") as file:
            self.__info = file.read()


    def save_info_to_file(self):
        """Сохранить общую информацию в файл

        :return: True, в случае успеха
        """

        if self.__filepath == "":
            self.__err_msg = "Не задан путь к файлу с информацией!"
            return False

        with open(self.__filepath, "w", encoding="utf-8") as file:
            file.write(self.__info)

        return True
