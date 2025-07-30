import wx
from cat_gamelist_mgr import CatGamelistMgr

class PnlCatGamesEditor(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Каталог игр
        self.__gamelist_mgr = CatGamelistMgr()

        # Текст последней ошибки
        self.__err_msg = ""

        # Рисуем интерфейс приложения
        # Основной sizer под 3 блока интерфейса
        self.__sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.__sizer_main)

        self.__stb_game_list = wx.StaticBox(self, wx.ID_ANY, "Список игр")
        self.__sizer_stb_game_list = wx.StaticBoxSizer(self.__stb_game_list, orient=wx.VERTICAL)
        self.__sizer_main.Add(self.__sizer_stb_game_list, 1, wx.TOP|wx.EXPAND, 0)

        self.__lb_games = wx.ListBox(self.__stb_game_list)
        self.__sizer_stb_game_list.Add(self.__lb_games, 1, wx.EXPAND)

        self.__stb_g_add_del = wx.StaticBox(self.__stb_game_list, wx.ID_ANY)
        self.__sizer_g_add_del = wx.StaticBoxSizer(self.__stb_g_add_del, orient=wx.HORIZONTAL)
        self.__sizer_stb_game_list.Add(self.__sizer_g_add_del, 0, wx.BOTTOM|wx.EXPAND)

        self.__sizer_g_add_del.AddStretchSpacer(prop=1)
        self.__btn_g_add = wx.Button(self.__stb_g_add_del, wx.ID_ANY, "Добавить")
        self.__sizer_g_add_del.Add(self.__btn_g_add, 0, wx.RIGHT)
        self.__btn_g_del = wx.Button(self.__stb_g_add_del, wx.ID_ANY, "Удалить")
        self.__sizer_g_add_del.Add(self.__btn_g_del, 0, wx.RIGHT)

        self.__stb_ctrls = wx.StaticBox(self, wx.ID_ANY)
        self.__sizer_stb_ctrls = wx.StaticBoxSizer(self.__stb_ctrls, orient=wx.HORIZONTAL)
        self.__sizer_main.Add(self.__sizer_stb_ctrls, 0, wx.BOTTOM|wx.EXPAND, 0)

        self.__sizer_stb_ctrls.AddStretchSpacer(prop=1)
        self.__btn_reset = wx.Button(self.__stb_ctrls, wx.ID_ANY, "Сброс")
        self.__sizer_stb_ctrls.Add(self.__btn_reset, 0, wx.RIGHT, border=5)
        self.__btn_reset.Bind(wx.EVT_BUTTON, self.btn_reset_click)

        self.__btn_save = wx.Button(self.__stb_ctrls, wx.ID_ANY, "Сохранить")
        self.__sizer_stb_ctrls.Add(self.__btn_save, 0, wx.RIGHT, border=5)
        self.__btn_save.Bind(wx.EVT_BUTTON, self.btn_save_click)


    def get_last_error(self):
        """Получить текст последней ошибки

        :return: Текст последней ошибки
        """

        return self.__err_msg


    def set_xml_file_path(self, filepath, reset_data = False):
        """Задать путь к XML файлу каталога игр

        :param filepath: Путь к XML файлу каталога игр
        :param reset_data: Сброс текущих данных
        :return: Функция не возвращает результат
        """

        if reset_data is True:
            # Удалим данные по играм
            self.__gamelist_mgr = CatGamelistMgr()

            # Очистим интерфейс
            self.__lb_games.Clear()

        self.__gamelist_mgr.set_xml_file_path(filepath)


    def reload_from_file(self):
        """Перезагрузить общую информацию из файла

        :return: True, в случае успеха
        """

        # Наполняем список игр
        self.__lb_games.Clear()

        if self.__gamelist_mgr.parse_xml_file() is False:
            self.__err_msg = self.__gamelist_mgr.get_last_error()
            return False

        for game_name in self.__gamelist_mgr.get_game_names():
            self.__lb_games.Append(game_name)

        return True


    def btn_reset_click(self, event):
        """Сбросить изменения каталога игр (перечитать с файлов)

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        return self.reload_from_file()


    def btn_save_click(self, event):
        """Сохранить сделанные изменения в файлы

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        if self.__gamelist_mgr.save_to_xml_file() is False:
            self.__err_msg = self.__gamelist_mgr.get_last_error()
            return False

        return True
