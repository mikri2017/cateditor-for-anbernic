from datetime import datetime
from lxml import etree

class GameInfoMgr():
    """Информация об игре"""

    def __init__(self):
        # Текст последней ошибки
        self.__err_msg = ""

        # Возможные теги с информацией в Anbernic и их типы
        self.__d_elem_types = {
            'path': str,
            'name': str,
            'desc': str,
            'image': str,
            'video': str,
            'marquee': str,
            'thumbnail': str,
            'rating': float, # 1.0 - это 100% ?
            'releasedate': datetime,
            'developer': str,
            'publisher': str,
            'genre': str, # Puzzle-Game - может, они какие-то конкретные?
            'players': int,
            'playcount': int,
            'lastplayed': datetime,
            'gametime': int, # В секундах
            'lang': str, # en, ru
            'crc32': str, # Хэши для контроля целостности
            'md5': str,
            'cheevosId': int,
            'cheevosHash': str
        }

        # Формат даты в XML теге
        self.__date_format = "%Y%m%dT%H%M%S" # 20190318T000000

        # Фактические значения атрибутов игры
        self.__d_elems = {}


    def get_last_error(self):
        """Получить последний текст ошибки

        :return: Строка с текстом ошибки
        """

        return self.__err_msg


    def get_possible_attribs(self):
        """Получить список возможных атрибутов c их типами

        :return: Словарь тег (атрибут игры) - его тип
        """

        return self.__d_elem_types


    def get_filled_attribs(self):
        """Получить список заполненных атрибутов игры

        :return: Словарь с атрибутами
        """

        return self.__d_elems


    def get_attrib_val(self, attrib_name):
        """Получить значение атрибута игры

        :param attrib_name: Наименование атрибута игры (тэг)
        :return: Значение атрибута, либо False, если такой не предусмотрен
        """

        if attrib_name not in self.__d_elem_types.keys():
            self.__err_msg = f"Атрибут {attrib_name} отсутствует"
            return False

        if attrib_name in self.__d_elems.keys():
            return self.__d_elems[attrib_name]

        if isinstance("", self.__d_elem_types[attrib_name]):
            return ""

        return None


    def set_attrib_val(self, attrib_name, attrib_val):
        """Задать значение атрибута игры

        :param attrib_name: Наименование атрибута игры (тэг)
        :param attrib_val: Значение атрибута игры
        :return: True, при успехе
        """

        if attrib_name not in self.__d_elem_types.keys():
            self.__err_msg = f"Атрибут {attrib_name} отсутствует"
            return False

        if not isinstance(attrib_val, self.__d_elem_types[attrib_name]):
            # Ожидается другой тип данных для атрибута
            self.__err_msg = f"Атрибут {attrib_name} должен иметь тип " \
                + f"{str(self.__d_elem_types[attrib_name])}"
            return False
        
        # Задаем значение атрибута игры
        self.__d_elems[attrib_name] = attrib_val


    def gen_xml_node(self):
        """Сгенерировать узел XML на основе имеющихся данных

        :return: XML узел (node)
        """

        xml_elem = etree.Element("game")
        for elem_tag, elem_val in self.__d_elems.items():
            if self.__d_elem_types[elem_tag] == datetime:
                elem_val = datetime.strftime(elem_val, self.__date_format)
            elif elem_tag in ["image", "video", "marquee", "thumbnail"]:
                # Изображения хранятся в отдельной папке images
                elem_val = f"./images/{elem_val}"
            elif elem_tag == "video":
                # Видео хранится в отдельной папке videos
                elem_val = f"./videos/{elem_val}"

            etree.SubElement(xml_elem, elem_tag).text = elem_val

        return xml_elem
