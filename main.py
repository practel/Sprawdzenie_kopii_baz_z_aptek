import win32serviceutil
import win32service
import win32event
import servicemanager
import Sprawdzanie_kopii_z_aptek
import sys
import time
from datetime import datetime

class SprKopii(win32serviceutil.ServiceFramework):
    _svc_name_ = 'SprKopii'
    _svc_display_name_ = 'SprKopii'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        self.isAlive = True

    def SvcStop(self):
        self.isAlive = False
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.isAlive = True
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.main()
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def main(self):
        # i = 0
        while self.isAlive:
            parametry_pobrane = Sprawdzanie_kopii_z_aptek.wczytaj_parametry("dane.ini")
            Sprawdzanie_kopii_z_aptek.uruchom(parametry_pobrane[0], parametry_pobrane[1])
            time.sleep(10)
    # pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(SprKopii)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        sys.frozen = 'windows_exe'  # Easier debugging
        win32serviceutil.HandleCommandLine(SprKopii)