import wx
import os

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

        # Рисуем интерфейс приложения
        self.stxt_cat_folder = wx.StaticText(self, -1, "Путь к папке с каталогом игр", (10, 25))
        self.txtctrl_cat_folder = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.Point(180, 20),
                                                wx.Size(475, -1), 0)

        self.btn_cat_folder_set = wx.Button(self, wx.ID_ANY, "Выбрать файл",
                                                     wx.Point(660, 20),
                                                     wx.Size(90, -1), 0)
        self.btn_cat_folder_set.Bind(wx.EVT_BUTTON, self.btn_cat_folder_set_click)


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


    def btn_cat_folder_set_click(self, event):
        folder_path_res = self.get_open_folder_path()
        if folder_path_res['res']:
            self.txtctrl_cat_folder.SetValue(folder_path_res['folder_path'])

            # Определяем наличие наших файлов в папке
            l_files = os.listdir(folder_path_res['folder_path'])
            for work_file, data in self.__d_files.items():
                if data['name'] in l_files:
                    self.__d_files[work_file]['exist'] = True

            print(self.__d_files)
