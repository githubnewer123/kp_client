# import win32gui,time,logging,win32api
# import win32con,pythoncom,win32com

class WindowsManager():

    def __int__(self):
        pass

    def getErrorCodeHandle(self, title):
        hld = win32gui.FindWindow(None, title)
        if hld > 0:
            dlg = win32gui.FindWindowEx(hld, None, 'Static', "--")
            return dlg

    def getErrorCode(self, handle):
        if handle:
            return win32gui.GetWindowText(handle)
        return "未知错误"

    def getMmptTitleName(self, timeout = 1):
        titles = set()
        def _getTitle(hwnd, nouse):
            if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
                titles.add(win32gui.GetWindowText(hwnd))
        stime = time.time()
        while True:
            if time.time() - stime > timeout:
                return None
            win32gui.EnumWindows(_getTitle, 0)
            lt = [t for t in titles if t]
            lt.sort()
            for t in lt:
                if "MMPT RF" in t:
                    return t

    def getMmptStatus(self, title):
        try:
            hld = win32gui.FindWindow(None, title)
            if hld > 0:
                # buffer = '0' * 50
                # txt_len = win32gui.SendMessage(hld, win32con.WA_CLICKACTIVE) + 1
                # print(txt_len)

                dlg = win32gui.FindWindowEx(hld, None, 'RICHEDIT', None)
                if dlg:
                    buf_size = win32gui.SendMessage(dlg, win32con.WM_GETTEXTLENGTH, 0, 0) + 1
                    str_buf = win32gui.PyMakeBuffer(buf_size+8)
                    win32api.SendMessage(dlg, win32con.WM_GETTEXT, buf_size+8, str_buf)
                    address, txt_len = win32gui.PyGetBufferAddressAndLen(str_buf[:buf_size-1])
                    text = win32gui.PyGetString(address, txt_len)
                    # print("Get MMPT status: %s"%(text))
                    return str(text).lower()
            return None
        except Exception as e:
            logging.info(str(e))
            return None

    def winMin(self, title):
        logging.info("窗口: %s最小化"%(title))
        pwin = win32gui.FindWindow(None, title)
        if pwin and not win32gui.IsIconic(pwin):
            win32gui.ShowWindow(pwin, win32con.SW_SHOWMINIMIZED)
            time.sleep(0.5)

    def winClose(self, title):
        logging.info("窗口: %s关闭"%(title))
        pwin = win32gui.FindWindow(None, title)
        if pwin:
            win32gui.SendMessage(pwin,win32con.WM_CLOSE,0,0)
            time.sleep(0.5)

    def clickButton(self,title, class_name, win_name):
        try:
            hld = win32gui.FindWindow(None, title)

            if hld > 0:
                dlg = win32gui.FindWindowEx(hld, None, class_name, win_name)
                if dlg:
                    win32gui.SendMessage(dlg, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
                    time.sleep(.100)
                    win32gui.SendMessage(dlg, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
        except Exception as e:
            logging.info(str(e))

    def winActive(self, title):
        try:
            logging.info("主窗口设置最上层")
            hwnd = win32gui.FindWindow(None, title)
            if hwnd <= 0:
                hwnd = win32gui.FindWindow(None, title)
            if hwnd:
                # pythoncom.CoInitialize()
                # shell = win32com.client.Dispatch("WScript.Shell")
                # shell.SendKeys('%')
                win32gui.SetForegroundWindow(hwnd)
                logging.info("主窗口设置最上层完成")
        except Exception as e:
            print(str(e))
            pass
