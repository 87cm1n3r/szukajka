from pathlib import Path

import wx
import wx.stc

import wojajo

cwd = Path(__file__).parents[0]

origin = ''
with open(str(cwd) + '/res/src.txt', encoding='UTF-8') as f:
    origin = f.read()
    f.close()

s_range = 20
top = 3
cur_pos = 0
j = 10


class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        pnl = wx.Panel(self)

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap("res/icon.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.textbox = wx.TextCtrl(pnl, size=(500, 30), pos=(10, 7), style=wx.TE_PROCESS_ENTER)
        self.bigbox = wx.stc.StyledTextCtrl(pnl, size=(590, 493), pos=(10, 41))
        self.bigbox.SetText(origin)
        bmp = wx.Bitmap("res/add.png", wx.BITMAP_TYPE_ANY)
        self.submitbutt = wx.BitmapButton(pnl, size=(80, 30), pos=(520, 7), bitmap=bmp)
        bmp = wx.Bitmap("res/undo.png", wx.BITMAP_TYPE_ANY)
        self.undobutt = wx.BitmapButton(pnl, size=(30, 30), pos=(610, 505), bitmap=bmp)
        bmp = wx.Bitmap("res/redo.png", wx.BITMAP_TYPE_ANY)
        self.redobutt = wx.BitmapButton(pnl, size=(30, 30), pos=(645, 505), bitmap=bmp)

        self.curr_arr = []
        self.overall_arr = []
        self.cur_pos = 0
        self.rew_arr = []

        # self.bigbox.BraceBadLight(30)
        self.suggestionlist = wx.ListCtrl(pnl, size=(165, 493), pos=(610, 7), style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.suggestionlist.InsertColumn(0, 'Słowo')
        self.suggestionlist.InsertColumn(1, 'Wynik')
        # self.suggestionlist.Append(('K', 10))
        # self.suggestionlist.Append(('Kurwa', 10))

        self.makeMenuBar()
        self.Bind(wx.EVT_TEXT, self.OnTextBox, self.textbox)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, self.submitbutt)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListSel, self.suggestionlist)
        self.Bind(wx.EVT_BUTTON, self.OnUndo, self.undobutt)
        self.Bind(wx.EVT_BUTTON, self.OnRedo, self.redobutt)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSubmit, self.textbox)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnListDbclick, self.suggestionlist)
        self.bigbox.StyleSetSpec(2, "back:#bcaaa4")
        self.bigbox.StyleSetSpec(3, "back:#ff7043")

    def OnUndo(self, event):
        try:
            self.rew_arr.append(self.overall_arr[-1])
            self.overall_arr.pop(-1)
            try:
                self.cur_pos = self.overall_arr[-1][-1]
            except IndexError:
                self.cur_pos = 0
            self.textbox.SetValue(self.textbox.GetValue())
        except IndexError:
            pass

    def OnRedo(self, event):
        try:
            self.overall_arr.append(self.rew_arr[-1])
            self.rew_arr.pop(-1)
            try:
                self.cur_pos = self.rew_arr[-1][-1]
            except IndexError:
                self.cur_pos = self.cur_pos = self.overall_arr[-1][-1]
            self.textbox.SetValue(self.textbox.GetValue())
        except IndexError:
            pass

    def highlight(self, pos, length=1, style=2):
        line = 1
        # Move to line
        self.bigbox.GotoLine(line - 1)
        # Get position
        pos = len(origin[:pos].encode('utf-8'))
        posend = pos
        for i in range(length):
            posend = self.bigbox.PositionAfter(posend)
        # Starts style at position pos
        self.bigbox.StartStyling(pos, 0xffff)
        # Until posend position, apply style 2
        self.bigbox.SetStyling(posend - pos, style)
        # Restore style 0 after the ending byte of the line
        self.bigbox.SetStyling(posend, 0)

    def makeMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)

    def OnSubmit(self, event):
        if len(self.curr_arr) > 0:
            # for x in self.curr_arr:
            #     self.overall_arr.append(x)
            self.overall_arr.append(self.curr_arr)
            self.cur_pos = self.curr_arr[-1] + 1
            self.textbox.SetValue('')
        else:
            pass

    def OnExit(self, event):
        self.Close(True)

    def Redraw(self):
        self.bigbox.ClearDocumentStyle()
        self.bigbox.SetWrapMode(wx.stc.STC_WRAP_WORD)
        for rar in self.overall_arr:
            for i in rar:
                self.highlight(i, style=3)

    def OnTextBox(self, event):
        st = event.GetString()

        arr = wojajo.szukaj_frazy(origin.lower(), st.lower(), l=self.cur_pos)
        self.curr_arr = arr
        self.Redraw()

        self.suggestionlist.ClearAll()
        self.suggestionlist.InsertColumn(0, 'Słowo')
        self.suggestionlist.InsertColumn(1, 'Wynik')
        self.k = wojajo.dopasowywanie_frazy(st, wojajo.wordlist, origin.lower(), N=30, l=self.cur_pos)

        if self.k:
            for chuj in self.k:
                self.suggestionlist.Append((chuj[0], chuj[1]))
        for i in arr:
            self.highlight(i)

    def OnListDbclick(self, event):
        self.curr_arr = self.k[event.Index][2]
        self.Redraw()
        for i in self.curr_arr:
            self.highlight(i)
        self.OnSubmit(event)

    def OnListSel(self, event):
        self.curr_arr = self.k[event.Index][2]
        self.Redraw()
        for i in self.curr_arr:
            self.highlight(i)


if __name__ == '__main__':
    app = wx.App()
    frm = MainFrame(None, title='Szukajka', size=wx.Size(800, 600))
    frm.Show()
    app.MainLoop()
