import wx
from wx.lib.newevent import NewCommandEvent
from datetime import datetime
from wx.adv import DatePickerCtrl, EVT_DATE_CHANGED, DP_DROPDOWN

# Событие изменения значения атрибута
chg_date_event, EVT_ATTRIB_DATE_CHG = NewCommandEvent()
chg_date_event = wx.NewEventType()
EVT_ATTRIB_DATE_CHG = wx.PyEventBinder(chg_date_event)

class ChgAttribDateEvent(wx.PyCommandEvent):
    """Событие изменения значения атрибута - даты
    """

    def __init__(self, obj, id = 0):
        super().__init__(chg_date_event, id)
        self.SetEventObject(obj)


class PnlAttribDateSet(wx.Panel):
    def __init__(self, parent, attr_name, attr_lbl, not_empty = False):
        """Инициализация класса

        :param parent: Ссылка на объект родителя
        :param attr_name: Наименование атрибута
        :param attr_lbl: Текст подписи атрибута
        :param not_empty: True - значение не может быть пустым
        :return: Функция не возвращает результат
        """

        wx.Panel.__init__(self, parent)

        # Название атрибута
        self.__attr_name = str(attr_name).strip()

        # Значение атрибута
        self.__dt_val = None

        # Может ли атрибут иметь пустое значение
        self.__not_empty = False
        if not_empty is True:
            self.__not_empty = True

        # Текст последней ошибки
        self.__err_msg = ""

        # Сайзер
        self.__sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.__sizer_main)

        # Подпись атрибута
        self.__stxt_gattr_desc = wx.StaticText(self)
        self.__stxt_gattr_desc.SetLabel(attr_lbl)
        self.__sizer_main.Add(self.__stxt_gattr_desc, 0, wx.LEFT, 5)

        # Выбор даты
        self.__dtpk_gattr_val = DatePickerCtrl(self, style=DP_DROPDOWN)
        self.__dtpk_gattr_val.SetRange(self.__dtpk_gattr_val.GetRange()[1], datetime.today())
        self.__sizer_main.Add(self.__dtpk_gattr_val, 1, wx.LEFT|wx.EXPAND, 5)
        self.__dtpk_gattr_val.Bind(EVT_DATE_CHANGED, self.__datepick_changed)

        # Флажок сброса значения параметра
        self.__chkbx_reset = wx.CheckBox(self)
        self.__chkbx_reset.SetLabel("Сбросить")
        self.__sizer_main.Add(self.__chkbx_reset, 0, wx.LEFT|wx.EXPAND, 5)
        self.__chkbx_reset.Bind(wx.EVT_CHECKBOX, self.__chkbx_reset_changed)

        # Проверка на возможность пустого значения
        if self.__not_empty is True:
            # Должно быть чем-то заполнено
            self.set_attrib_val(datetime.today())
            self.__chkbx_reset.Enabled = False
            self.__dtpk_gattr_val.Enabled = True
        else:
            self.__chkbx_reset.Enabled = True
            self.__chkbx_reset.Value = True
            self.__dtpk_gattr_val.Enabled = False


    def __datepick_changed(self, event):
        """Дата изменилась, правим значение атрибута

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        dtpk = event.GetEventObject()

        # Преобразуем wx.DateTime в datetime
        date_format = "%Y-%m-%d"
        self.__dt_val = datetime.strptime(
            dtpk.GetValue().Format(date_format),
            date_format
        )

        # Генерируем событие изменения даты
        wx.PostEvent(
            self.GetEventHandler(),
            ChgAttribDateEvent(self, self.GetId())
        )


    def __chkbx_reset_changed(self, event):
        """Изменилось состояния флажка сброса даты

        :param event: Событие элемента графического интерфейса
        :return: Функция не возвращает результат
        """

        chkbx = event.GetEventObject()
        if chkbx.Value is True:
            # Включен сброс, блокируем выбор даты
            self.__dtpk_gattr_val.Enabled = False
        else:
            # Возвращаем возможность выбора даты
            self.__dtpk_gattr_val.Enabled = True

            # Если значения нет, ставим дату как в интерфейсе
            if self.__dt_val is None:
                # Преобразуем wx.DateTime в datetime
                date_format = "%Y-%m-%d"
                self.__dt_val = datetime.strptime(
                    self.__dtpk_gattr_val.GetValue().Format(date_format),
                    date_format
                )

        # Генерируем событие изменения даты
        wx.PostEvent(
            self.GetEventHandler(),
            ChgAttribDateEvent(self, self.GetId())
        )


    def get_last_error(self):
        """Получить текст последней ошибки

        :return: Текст последней ошибки
        """

        return self.__err_msg


    def get_attrib_name(self):
        """Получить значение атрибута

        :return: Наименование атрибута
        """

        return self.__attr_name


    def get_attrib_val(self):
        """Получить значение атрибута

        :return: datetime - текущее значение атрибута
        """

        if self.__chkbx_reset.Value is True:
            return None

        return self.__dt_val


    def set_attrib_val(self, dt_val):
        """Задать значение атрибута

        :param dt_val: datetime, как значение атрибута
        :return: True, в случае успеха
        """

        if (dt_val is None) and (not self.__not_empty):
            self.__chkbx_reset.Value = True
            self.__dtpk_gattr_val.Enabled = False
        elif isinstance(dt_val, datetime):
            self.__chkbx_reset.Value = False
            self.__dtpk_gattr_val.Enabled = True
            self.__dt_val = dt_val

            # Устанавливаем значение даты на интерфейсе
            self.__dtpk_gattr_val.SetValue(dt_val.date())
        else:
            self.__err_msg = "Значение атрибута должно иметь тип datetime"
            return False

        return True
