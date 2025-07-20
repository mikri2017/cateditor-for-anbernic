class CatInfoMgr():
    """Общая информацию о каталоге игр"""

    def __init__(self):
        self.__info = ""


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
