import os
from game_info_mgr import GameInfoMgr
from lxml import etree

class CatGamelistMgr():
    """Список игр"""

    def __init__(self):
        """Инициализация класса

        :return: Функция не возвращает результат
        """

        # Путь к XML файлу
        self.__filepath = ""

        # Словарь с данными по играм
        self.__d_gamelist = {}

        # Текст последней ошибки
        self.__err_mgr = ""


    def get_last_error(self):
        """Получить текст последней ошибки

        :return: Текст последней ошибки
        """

        return self.__err_mgr


    def get_xml_file_path(self):
        """Получить путь к используемому XML файлу каталога игр

        :return: Путь к файлу
        """

        return self.__filepath


    def set_xml_file_path(self, filepath):
        """Задать путь к XML файлу каталога игр

        :param filepath: Путь к XML файлу
        :return: Функция не возвращает результат
        """

        self.__filepath = str(filepath).strip()


    def parse_xml_file(self):
        """Распарсить XML файл каталога игр в список

        :return: True, в случае успеха
        """

        if not os.path.exists(self.__filepath):
            self.__err_mgr = f"Файл {self.__filepath} не существует"
            return False
        
        tree = etree.parse(self.__filepath)
        root = tree.getroot()
        if root.tag != "gameList":
            self.__err_mgr = f"Неожиданный корневой элемент {root.tag}! " \
                + f"Ожидается <gameList>"
            return False
        
        for game_elem in root:
            if game_elem.tag == "game":
                game_inf = GameInfoMgr()
                for game_inf_tag in game_elem:
                    game_inf.set_attrib_val(game_inf_tag.tag, game_inf_tag.text)

                self.__d_gamelist[game_inf.get_attrib_val("name")] = game_inf

        return True


    def get_game_names(self):
        """Получить список названий доступных игр

        :return: Список названий доступных игр
        """

        # Сортирум словарь
        self.__d_gamelist = dict(sorted(self.__d_gamelist.items()))

        # Отправляем список названий игр
        return list(self.__d_gamelist.keys())


    def get_game_attribs(self, name):
        """Получить атрибуты игры по её названию

        :param name: Наименование игры
        :return: Словарь атрибутов игры
        """

        if "name" in self.__d_gamelist.keys():
            return self.__d_gamelist[name].get_filled_attribs()
        else:
            return {}


    def set_game_attribs(self, d_attribs):
        """Задать атрибуты игры по её названию

        :param d_attribs: Словарь с атрибутами игры
        :return: True, в случае успеха
        """

        if "name" not in d_attribs.keys():
            self.__err_mgr = "Отсутствует атрибут 'name' - название игры!"
            return False
        
        d_attribs['name'] = str(d_attribs['name']).strip()

        game_inf = GameInfoMgr()
        for attrib_name, attrib_val in d_attribs.items():
            game_inf.set_attrib_val(attrib_name, attrib_val)

        self.__d_gamelist[d_attribs['name']] = game_inf
        return True


    def save_to_xml_file(self):
        """Сохранить список игр в XML файл каталога

        :return: True, в случае успеха
        """

        root = etree.Element("gameList")
        for name, game_inf in self.__d_gamelist.items():
            root.append(game_inf.gen_xml_node())

        with open(self.__filepath, "w", encoding="UTF-8") as file:
            xml_file_str = etree.tostring(
                root,
                encoding="UTF-8",
                pretty_print=True
            ).decode("UTF-8")

            file.write(xml_file_str)

        return True
