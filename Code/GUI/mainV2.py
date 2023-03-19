import wx

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Blinduino')

        self.SetMinSize((800, 600))

        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.HORIZONTAL)


        # Columna izquierda
        col_izquierda = wx.Panel(panel)
        col_izquierda.SetBackgroundColour('#432D5C')

        modulo_label = wx.StaticText(col_izquierda, label='Modulo', style=wx.ALIGN_CENTER)
        modulo_label.SetForegroundColour('#ffffff')
        modulo_label.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        col_izquierda_sizer = wx.BoxSizer(wx.VERTICAL)
        col_izquierda_sizer.AddStretchSpacer()
        col_izquierda_sizer.Add(modulo_label, flag=wx.ALIGN_CENTER)
        col_izquierda_sizer.AddStretchSpacer()

        col_izquierda.SetSizer(col_izquierda_sizer)
        sizer.Add(col_izquierda, flag=wx.EXPAND|wx.ALL, border=0)

        # Columna derecha superior
        col_derecha = wx.Panel(panel)
        col_derecha_sizer = wx.BoxSizer(wx.VERTICAL)
#        col_derecha_up.SetBackgroundColour('#614B79')

        descripcion_label = wx.StaticText(panel, label='Descripción', style=wx.ALIGN_CENTER)
        descripcion_label.SetForegroundColour('#ffffff')
        descripcion_label.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
 
        col_derecha_sizer.AddStretchSpacer()
        col_derecha_sizer.Add(descripcion_label, flag=wx.ALIGN_CENTER)
        col_derecha_sizer.AddStretchSpacer()

        col_derecha.SetSizer(col_derecha_sizer)
        sizer.Add(col_derecha, pos=(0, 0), span=(2, 1), flag=wx.EXPAND|wx.ALL, border=0)


        # Columna derecha inferior
        pin_label = wx.StaticText(panel, label='Pin 1', style=wx.ALIGN_CENTER)
        pin_label.SetForegroundColour('#432D5C')
        pin_label.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        sizer.Add(pin_label, pos=(1, 1), flag=wx.EXPAND|wx.ALL, border=0)

        # Configurar la expansión del sizer
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)

        panel.SetSizer(sizer)
        sizer.Fit(self)

        self.Show(True)


if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()
