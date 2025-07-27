import wx
import os
from cat_info_mgr import CatInfoMgr
from cat_gamelist_mgr import CatGamelistMgr

class PnlMainFrm(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Рабочие файлы каталога
        self.__d_files = {
            'info': {
                'exist': False,
                'name': "_info.txt"
            },
            'gamelist': {
                'exist': False,
                'name': "gamelist.xml"
            }
        }

        # Общая информация
        self.__info_mgr = CatInfoMgr()

        # Каталог игр
        self.__gamelist_mgr = CatGamelistMgr()

        # Рисуем интерфейс приложения
        # Основной sizer под 3 блока интерфейса
        self.__sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.__sizer_main)

        # Блок 1. Выбор папки с каталогом игр
        self.__stb_path = wx.StaticBox(self, wx.ID_ANY, "")
        self.__sizer_stb_path = wx.StaticBoxSizer(self.__stb_path, orient=wx.HORIZONTAL)
        self.__sizer_main.Add(self.__sizer_stb_path, 0, wx.TOP|wx.EXPAND)

        # Блок 2. Редактор каталога игр
        self.__stb_games_cat = wx.StaticBox(self, wx.ID_ANY, "Редактор каталога игр")
        self.__sizer_stb_games_cat = wx.StaticBoxSizer(self.__stb_games_cat, orient=wx.VERTICAL)
        self.__sizer_main.Add(self.__sizer_stb_games_cat, 1, wx.TOP|wx.EXPAND, 0)

        # Блок 3. Сообщения о проблемах
        self.__stb_warn_msgs = wx.StaticBox(self, wx.ID_ANY, "Сообщения об ошибках")
        self.__stb_warn_msgs.SetMaxSize((-1, 150))
        self.__sizer_main.Add(self.__stb_warn_msgs, 1, wx.BOTTOM|wx.EXPAND)

        # Заполняем элементами Блок 1
        # Строка пояснения
        self.__stxt_cat_folder = wx.StaticText(
            self.__stb_path,
            wx.ID_ANY,
            "Путь к папке\nс каталогом игр"
        )

        self.__sizer_stb_path.Add(self.__stxt_cat_folder, 0, wx.LEFT, border=5)

        # Поле с путем до папки каталога
        self.__txtctrl_cat_folder = wx.TextCtrl(
            self.__stb_path,
            wx.ID_ANY,
            wx.EmptyString
        )

        self.__sizer_stb_path.Add(self.__txtctrl_cat_folder, 1, wx.LEFT|wx.EXPAND, border=5)

        # Кнопка выбора папки
        self.__btn_cat_folder_set = wx.Button(self.__stb_path, wx.ID_ANY, "Обзор")
        self.__sizer_stb_path.Add(self.__btn_cat_folder_set, 0, wx.RIGHT|wx.EXPAND, border=5)
        self.__btn_cat_folder_set.Bind(wx.EVT_BUTTON, self.btn_cat_folder_set_click)

        # Заполняем элементами Блок 2
        self.__pnl_gc_editor = wx.Panel(self.__stb_games_cat)
        self.__bsizer_gc_editor = wx.BoxSizer(wx.HORIZONTAL)
        self.__pnl_gc_editor.SetSizer(self.__bsizer_gc_editor)
        self.__sizer_stb_games_cat.Add(self.__pnl_gc_editor, 1, wx.TOP|wx.EXPAND)

        self.__pnl_gc_ctrl = wx.Panel(self.__stb_games_cat)
        self.__bsizer_gc_ctrl = wx.BoxSizer(wx.HORIZONTAL)
        self.__pnl_gc_ctrl.SetSizer(self.__bsizer_gc_ctrl)
        self.__sizer_stb_games_cat.Add(self.__pnl_gc_ctrl, 0, wx.BOTTOM|wx.EXPAND)

        # Кнопки управления редактором
        self.__bsizer_gc_ctrl.AddStretchSpacer(prop=1)

        self.__btn_gc_reset = wx.Button(self.__pnl_gc_ctrl, wx.ID_ANY, "Сброс")
        self.__bsizer_gc_ctrl.Add(self.__btn_gc_reset, 0, wx.RIGHT, border=5)
        self.__btn_gc_reset.Bind(wx.EVT_BUTTON, self.btn_gc_reset_click)

        self.__btn_gc_save = wx.Button(self.__pnl_gc_ctrl, wx.ID_ANY, "Сохранить")
        self.__bsizer_gc_ctrl.Add(self.__btn_gc_save, 0, wx.RIGHT, border=5)
        self.__btn_gc_save.Bind(wx.EVT_BUTTON, self.btn_gc_save_click)

        # Список игр
        self.__stb_game_list = wx.StaticBox(self.__pnl_gc_editor, wx.ID_ANY, "Игры")
        self.__sizer_stb_game_list = wx.StaticBoxSizer(self.__stb_game_list, orient=wx.HORIZONTAL)
        self.__bsizer_gc_editor.Add(self.__sizer_stb_game_list, 1, wx.LEFT|wx.EXPAND)

        self.__lb_games = wx.ListBox(self.__stb_game_list)
        self.__sizer_stb_game_list.Add(self.__lb_games, 0, wx.EXPAND)


    def get_open_folder_path(self):
        res = {
            'res': True,
            'folder_path': ""
        }

        with wx.DirDialog(
            self,
            "Выбрать папку каталога игр"
        ) as dir_dlg:
            if dir_dlg.ShowModal() == wx.ID_CANCEL:
                res['res'] = False
                return res

            res['folder_path'] = dir_dlg.GetPath()

        return res


    def __reload_from_files(self):
        """Загрузка информации о каталоге с файлов

        :return: Функция не возвращает результат
        """

        folder_path = self.__txtctrl_cat_folder.GetValue()
        if folder_path == "":
            header = f"Редактор каталога игр Anbernic"
            msg = "Не выбран путь к папке каталога игр!"
            wx.MessageBox(msg, header, wx.OK | wx.ICON_ERROR)
            return

        # Определяем наличие наших файлов в папке
        l_files = os.listdir(folder_path)
        for work_file, data in self.__d_files.items():
            if data['name'] in l_files:
                self.__d_files[work_file]['exist'] = True

        # Общая информация о каталоге игр
        info_file = self.__d_files['info']['name']
        info_path = os.path.join(folder_path, info_file)

        self.__info_mgr.set_file_path(info_path)
        if self.__d_files['info']['exist'] is True:
            self.__info_mgr.load_info_from_file()

        # Каталог игр
        gamelist_file = self.__d_files['gamelist']['name']
        gamelist_path = os.path.join(folder_path, gamelist_file)

        self.__gamelist_mgr.set_xml_file_path(gamelist_path)
        if self.__d_files['gamelist']['exist'] is True:
            self.__gamelist_mgr.parse_xml_file()

        # Наполняем список игр
        self.__lb_games.Clear()
        for game_name in self.__gamelist_mgr.get_game_names():
            self.__lb_games.Append(game_name)

        print("Информация:")
        print(self.__info_mgr.get_info())


    def btn_cat_folder_set_click(self, event):
        """Выбор папки и загрузка информационных файлов каталога

        :param event:
        :return: Функция не возвращает результат
        """

        folder_path_res = self.get_open_folder_path()
        if folder_path_res['res']:
            self.__txtctrl_cat_folder.SetValue(folder_path_res['folder_path'])
            self.__reload_from_files()


    def btn_gc_reset_click(self, event):
        """Сбросить изменения каталога игр (перечитать с файлов)

        :param event:
        :return: Функция не возвращает результат
        """

        self.__reload_from_files()


    def btn_gc_save_click(self, event):
        """Сохранить сделанные изменения в файлы

        :param event:
        :return: Функция не возвращает результат
        """

        folder_path = self.__txtctrl_cat_folder.GetValue()
        if folder_path == "":
            header = f"Редактор каталога игр Anbernic"
            msg = "Не выбран путь к папке каталога игр!"
            wx.MessageBox(msg, header, wx.OK | wx.ICON_ERROR)
            return

        # Сохраняем информацию о каталоге
        pass

        # Сохраняем каталог игр
        self.__gamelist_mgr.save_to_xml_file()
