import os
import sys
import wx
import time
from pnl_main_frm import PnlMainFrm

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="CatEditor For Anbernic")
        self.pnl = PnlMainFrm(self)


if __name__ == "__main__":
    # Инициализация приложения

    # Делаем папку расположения exe'шника скрипта рабочей
    work_dir = os.path.dirname(sys.executable)
    os.chdir(work_dir)

    log_folder_path = "logs"

    if not os.path.exists(log_folder_path):
        try:
            os.makedirs(log_folder_path)
        except Exception as ex:
            error_msg = "Не удалось создать папку %s\r\n\r\n%s" % (
                log_folder_path,
                str(ex)
            )

            print(error_msg)
            time.sleep(10)
            sys.exit(1)

    print("Скрипт запустил работу")

    info_msg = "Рабочая папка: %s" % work_dir
    print(info_msg)

    app = wx.App()
    MainFrame().Show()
    app.MainLoop()

    print("Скрипт завершил работу")
