import wx
from cat_info_mgr import CatInfoMgr

class PnlCatInfo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Общая информация
        self.__info_mgr = CatInfoMgr()

        # Текст последней ошибки
        self.__err_msg = ""

        # Рисуем интерфейс приложения
        # Основной sizer под 3 блока интерфейса
        self.__sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.__sizer_main)

        self.__txt_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.__sizer_main.Add(self.__txt_ctrl, 1, wx.TOP|wx.EXPAND, 10)
        self.__txt_ctrl.Bind(wx.EVT_TEXT, self.txt_ctrl_update_info)

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


    def get_file_path(self):
        """Получить путь к файлу с информацией

        :return: Путь к файлу
        """

        return self.__info_mgr.get_file_path()


    def set_file_path(self, filepath):
        """Задать путь к файлу с информацией

        :param filepath: Путь к текстовому файлу с информацией
        :return: Функция не возвращает результат
        """

        self.__info_mgr.set_file_path(filepath)


    def reload_from_file(self):
        """Перезагрузить общую информацию из файла

        :return: True, в случае успеха
        """

        self.__txt_ctrl.Clear()

        if self.__info_mgr.load_info_from_file() is False:
            self.__err_msg = self.__info_mgr.get_last_error()
            return False

        self.__txt_ctrl.WriteText(self.__info_mgr.get_info())
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

        if self.__info_mgr.save_info_to_file() is False:
            self.__err_msg = self.__info_mgr.get_last_error()
            return False

        return True


    def txt_ctrl_update_info(self, event):
        """Изменение общей информации при её редактировании
        в интерфейсе приложения

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        txt_ctrl = event.GetEventObject()
        self.__info_mgr.set_info(txt_ctrl.GetValue())
