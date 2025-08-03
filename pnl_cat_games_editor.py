import wx
from wx.lib.scrolledpanel import ScrolledPanel
from wx.lib.agw.floatspin import FloatSpin
from wx.adv import DatePickerCtrl, EVT_DATE_CHANGED
from datetime import datetime
from cat_gamelist_mgr import CatGamelistMgr

class PnlCatGamesEditor(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Каталог игр
        self.__gamelist_mgr = CatGamelistMgr()

        # Текущая выбранная игра
        self.__selected_game = ""

        # Список заполненния атрибутов игры в интерфейсе
        # Эдемент списка - список с элементами под индексами:
        # 0 - наименование атрибута, 1 и далее - элементы интерфейса
        self.__l_gattrs = []

        # Индикатор, что поля заполняются не пользователем
        self.__ignore_chg_attrib = False

        # Текст последней ошибки
        self.__err_msg = ""

        # Рисуем интерфейс приложения
        # Основной sizer под 3 блока интерфейса
        self.__sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.__sizer_main)

        self.__pnl_ed = wx.Panel(self)
        self.__sizer_pnl_main = wx.BoxSizer(wx.HORIZONTAL)
        self.__pnl_ed.SetSizer(self.__sizer_pnl_main)
        self.__sizer_main.Add(self.__pnl_ed, 1, wx.TOP|wx.EXPAND)

        self.__stb_game_list = wx.StaticBox(self.__pnl_ed, wx.ID_ANY, "Список игр")
        self.__sizer_stb_game_list = wx.StaticBoxSizer(self.__stb_game_list, orient=wx.VERTICAL)
        self.__sizer_pnl_main.Add(self.__sizer_stb_game_list, 1, wx.TOP|wx.EXPAND, 0)

        self.__lb_games = wx.ListBox(self.__stb_game_list)
        self.__sizer_stb_game_list.Add(self.__lb_games, 1, wx.EXPAND)
        self.__lb_games.Bind(wx.EVT_LISTBOX, self.lb_games_selected)

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

        # Заполняем блок атрибутов
        self.__stb_game_attrs = wx.StaticBox(self.__pnl_ed, wx.ID_ANY, "Атрибуты игры")
        self.__sizer_stb_game_attr = wx.StaticBoxSizer(self.__stb_game_attrs, orient=wx.VERTICAL)
        self.__sizer_pnl_main.Add(self.__sizer_stb_game_attr, 3, wx.EXPAND, 0)

        self.__scrl_pnl_attrs = ScrolledPanel(self.__stb_game_attrs)
        self.__scrl_pnl_attrs.SetupScrolling(False)
        self.__sizer_scrl_pnl_attrs = wx.BoxSizer(wx.VERTICAL)
        self.__scrl_pnl_attrs.SetSizer(self.__sizer_scrl_pnl_attrs)
        self.__sizer_stb_game_attr.Add(self.__scrl_pnl_attrs, 1, wx.EXPAND)

        # Заполняем интерфейс атрибутами и их значениями
        self.reload_game_attrs()


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
            self.__selected_game = ""

        self.__gamelist_mgr.set_xml_file_path(filepath)


    def reload_from_file(self, selected_game = ""):
        """Перезагрузить общую информацию из файла

        :param selected_game: Наименование выбранной игры
        :return: True, в случае успеха
        """

        # Сбросим элементы интерфейса
        self.__lb_games.Clear()
        self.__selected_game = ""
        self.reload_game_attrs()

        # Наполняем список игр
        if self.__gamelist_mgr.parse_xml_file() is False:
            self.__err_msg = self.__gamelist_mgr.get_last_error()
            return False

        selected_id = 0
        for game_name in self.__gamelist_mgr.get_game_names():
            self.__lb_games.Append(game_name)
            if game_name == selected_game:
                selected_id = self.__lb_games.FindString(selected_game)

        self.__lb_games.SetSelection(selected_id)
        self.__selected_game = self.__lb_games.GetString(selected_id)
        self.reload_game_attrs()
        return True


    def reload_game_attrs(self):
        """Заполнить атрибуты игры в интерфейсе

        :return: Функция не возвращает результат
        """

        # Отмечаем, что заполнение происходит не пользователем
        self.__ignore_chg_attrib = True

        # Получаем возможные атрибуты игры
        d_all_game_attrs = self.__gamelist_mgr.get_game_attribs(False)

        d_game_attrs = {}
        if self.__selected_game != "":
            d_game_attrs = self.__gamelist_mgr.get_game_attribs(True, self.__selected_game)

        i = 0
        for attr_name, attr_type in d_all_game_attrs.items():
            # Список атрибута
            l_attr = []
            l_attr.append(attr_name) # 0-м всегда наименование атрибута

            if len(self.__l_gattrs) < i + 1:
                # Элемента интерфейса еще нет, добавляем
                pnl_game_attr = wx.Panel(self.__scrl_pnl_attrs)
                sizer_pnl_game_attr = wx.BoxSizer(wx.HORIZONTAL)
                pnl_game_attr.SetSizer(sizer_pnl_game_attr)
                l_attr.append(pnl_game_attr)

                stxt_gattr_desc = wx.StaticText(pnl_game_attr)
                stxt_gattr_desc.SetLabel(attr_name)
                sizer_pnl_game_attr.Add(stxt_gattr_desc, 0, wx.LEFT, 5)
                l_attr.append(stxt_gattr_desc)

                # Назначаем элемент интерфейса, в зависимости от его типа
                if attr_type == int:
                    spnctrl_gattr_val = wx.SpinCtrl(pnl_game_attr)
                    spnctrl_gattr_val.SetName(attr_name)
                    spnctrl_gattr_val.SetMax(1000000)
                    sizer_pnl_game_attr.Add(spnctrl_gattr_val, 1, wx.LEFT|wx.EXPAND, 5)
                    spnctrl_gattr_val.Bind(wx.EVT_SPINCTRL, self.spnctrl_changed)
                    l_attr.append(spnctrl_gattr_val)

                    # Флажок сброса значения параметра
                    chkbx_reset = wx.CheckBox(pnl_game_attr)
                    chkbx_reset.SetLabel("Сбросить")
                    chkbx_reset.Enabled = False
                    sizer_pnl_game_attr.Add(chkbx_reset, 0, wx.LEFT|wx.EXPAND, 5)
                    l_attr.append(chkbx_reset)
                elif attr_type == float:
                    fspn_gattr_val = FloatSpin(pnl_game_attr, digits=2)
                    fspn_gattr_val.SetName(attr_name)
                    fspn_gattr_val.SetMax(1000000)
                    sizer_pnl_game_attr.Add(fspn_gattr_val, 1, wx.LEFT|wx.EXPAND, 5)
                    fspn_gattr_val.Bind(wx.EVT_SPINCTRL, self.fspn_changed)
                    l_attr.append(fspn_gattr_val)

                    # Флажок сброса значения параметра
                    chkbx_reset = wx.CheckBox(pnl_game_attr)
                    chkbx_reset.SetLabel("Сбросить")
                    chkbx_reset.Enabled = False
                    sizer_pnl_game_attr.Add(chkbx_reset, 0, wx.LEFT|wx.EXPAND, 5)
                    l_attr.append(chkbx_reset)
                elif attr_type == datetime:
                    dtpk_gattr_val = DatePickerCtrl(pnl_game_attr, style=wx.adv.DP_DROPDOWN)
                    dtpk_gattr_val.SetName(attr_name)
                    dtpk_gattr_val.SetRange(dtpk_gattr_val.GetRange()[1], datetime.today())
                    sizer_pnl_game_attr.Add(dtpk_gattr_val, 1, wx.LEFT|wx.EXPAND, 5)
                    dtpk_gattr_val.Bind(EVT_DATE_CHANGED, self.datepick_changed)
                    l_attr.append(dtpk_gattr_val)

                    # Флажок сброса значения параметра
                    chkbx_reset = wx.CheckBox(pnl_game_attr)
                    chkbx_reset.SetLabel("Сбросить")
                    chkbx_reset.Enabled = False
                    sizer_pnl_game_attr.Add(chkbx_reset, 0, wx.LEFT|wx.EXPAND, 5)
                    l_attr.append(chkbx_reset)
                else:
                    txtctrl_gattr_val = wx.TextCtrl(pnl_game_attr)
                    txtctrl_gattr_val.SetName(attr_name)
                    sizer_pnl_game_attr.Add(txtctrl_gattr_val, 1, wx.LEFT|wx.EXPAND, 5)
                    txtctrl_gattr_val.Bind(wx.EVT_TEXT, self.txtctrl_changed)
                    l_attr.append(txtctrl_gattr_val)

                self.__sizer_scrl_pnl_attrs.Add(pnl_game_attr, 1, wx.TOP|wx.EXPAND, 5)
            else:
                l_attr = self.__l_gattrs[i]

            # Заполняем значение атрибута
            if attr_name in d_game_attrs.keys():
                # Элемент интерфейса, хранящий значение
                if isinstance(l_attr[3], wx.SpinCtrl) \
                    or isinstance(l_attr[3], FloatSpin):
                    l_attr[3].SetValue(d_game_attrs[attr_name])
                elif isinstance(l_attr[3], DatePickerCtrl):
                    l_attr[3].SetValue(d_game_attrs[attr_name].date())
                else:
                    l_attr[3].SetValue(str(d_game_attrs[attr_name]))

                l_attr[3].SetBackgroundColour(wx.WHITE)
                l_attr[3].Refresh()
            else:
                # Элемент интерфейса, хранящий значение
                if isinstance(l_attr[3], wx.SpinCtrl) \
                    or isinstance(l_attr[3], FloatSpin):
                    l_attr[3].SetValue(0)
                elif isinstance(l_attr[3], DatePickerCtrl):
                    # Если есть время, дату не установить
                    l_attr[3].SetValue(datetime.today().date())
                else:
                    l_attr[3].SetValue("")

            if len(self.__l_gattrs) < i + 1:
                self.__l_gattrs.append(l_attr)
            else:
                self.__l_gattrs[i] = l_attr

            i += 1

        # Дальше менять значение будет пользователь
        self.__ignore_chg_attrib = False


    def lb_games_selected(self, event):
        """Реакция на выбор игры из списка

        :return: Функция не возвращает результат
        """

        lb = event.GetEventObject()
        self.__game_id_lb = lb.GetSelection()
        self.__selected_game = lb.GetString(self.__game_id_lb)

        # Сброс и загрузка атрибутов игры
        self.reload_game_attrs()


    def spnctrl_changed(self, event):
        """Изменилось числовое свойство игры

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        if self.__selected_game != "":
            if self.__ignore_chg_attrib is False:
                # Пользователь изменил атрибут игры,
                # применяем его к списку игр
                spnctrl = event.GetEventObject()
                attr_name = spnctrl.GetName()
                attr_val = spnctrl.GetValue()
                self.__gamelist_mgr.set_game_attrib(
                    self.__selected_game,
                    attr_name,
                    attr_val
                )


    def fspn_changed(self, event):
        """Изменилось числовое дробное свойство игры

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        if self.__selected_game != "":
            if self.__ignore_chg_attrib is False:
                # Пользователь изменил атрибут игры,
                # применяем его к списку игр
                spnctrl = event.GetEventObject()
                attr_name = spnctrl.GetName()
                attr_val = spnctrl.GetValue()
                self.__gamelist_mgr.set_game_attrib(
                    self.__selected_game,
                    attr_name,
                    attr_val
                )


    def datepick_changed(self, event):
        """Изменилось свойство игры, представленное датой

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        if self.__selected_game != "":
            if self.__ignore_chg_attrib is False:
                # Пользователь изменил атрибут игры,
                # применяем его к списку игр
                dtpk = event.GetEventObject()
                attr_name = dtpk.GetName()

                # Преобразуем wx.DateTime в datetime
                date_format = "%Y-%m-%d"
                attr_val = datetime.strptime(
                    dtpk.GetValue().Format(date_format),
                    date_format
                )

                self.__gamelist_mgr.set_game_attrib(
                    self.__selected_game,
                    attr_name,
                    attr_val
                )


    def txtctrl_changed(self, event):
        """Изменился текст свойства игры

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        if self.__selected_game != "":
            if self.__ignore_chg_attrib is False:
                # Пользователь изменил атрибут игры,
                # применяем его к списку игр
                txtctrl = event.GetEventObject()
                attr_name = txtctrl.GetName()
                attr_val = txtctrl.GetValue()
                if attr_name in ["path", "name"]:
                    # Нельзя оставлять пустыми основные атрибуты
                    if attr_val.strip() == "":
                        txtctrl.SetBackgroundColour(wx.RED)
                        txtctrl.Refresh()
                    else:
                        txtctrl.SetBackgroundColour(wx.WHITE)
                        txtctrl.Refresh()

                if txtctrl.GetBackgroundColour() == wx.WHITE:
                    # Изменение цвета поля говорит об ошибке
                    # Сохраняем только поле с пустым фоновым цветом
                    self.__gamelist_mgr.set_game_attrib(
                        self.__selected_game,
                        attr_name,
                        attr_val
                    )


    def btn_reset_click(self, event):
        """Сбросить изменения каталога игр (перечитать с файлов)

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        id_sel = self.__lb_games.GetSelection()
        self.__selected_game = ""
        if id_sel != -1:
            self.__selected_game = self.__lb_games.GetString(id_sel)
            return self.reload_from_file(self.__selected_game)

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
