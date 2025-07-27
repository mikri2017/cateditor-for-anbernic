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

            # 
            info_file = self.__d_files['info']['name']
            info_path = os.path.join(
                folder_path_res['folder_path'],
                info_file
            )

            self.__info_mgr.set_file_path(info_path)
            if self.__d_files['info']['exist'] is True:
                self.__info_mgr.load_info_from_file()

            # Каталог игр
            gamelist_file = self.__d_files['gamelist']['name']

            gamelist_path = os.path.join(
                folder_path_res['folder_path'],
                gamelist_file
            )

            self.__gamelist_mgr.set_xml_file_path(gamelist_path)
            if self.__d_files['gamelist']['exist'] is True:
                self.__gamelist_mgr.parse_xml_file()


            print("Информация:")
            print(self.__info_mgr.get_info())

            print("Игры:")
            print(self.__gamelist_mgr.get_game_names())

            # self.__gamelist_mgr.save_to_xml_file()
