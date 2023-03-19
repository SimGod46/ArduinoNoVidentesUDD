from recognize import modules_recognizer
from dbms import data_manager
import voice,cv2,wx

class Controller:
    def __init__(self):
        self.cap = cv2.VideoCapture(1) #Cambiar a 1 para utilizar arduino
        self.reconocedor_img = modules_recognizer()
        self.base_datos = data_manager()
#        height = 224#int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#        width = 224#int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    def take_photo(self):
            ret, frame = self.cap.read()
            cv2.imwrite('module.jpg',frame)
            cv2.imshow('image',frame)
            # reconocimiento
            module_detected= self.reconocedor_img.read('module.jpg')
            print('Detectado: ',module_detected)
            module_info = self.base_datos.query_module(module_detected) #
            voice.q.put(module_info)
            print('_____')
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Blinduino')

        self.SetMinSize((800, 600))
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(hgap=0, vgap=0)

        # Columna izquierda
        col_izquierda = wx.Panel(panel)
        col_izquierda.SetBackgroundColour('#432D5C')

        self.modulo_label = wx.StaticText(col_izquierda, label='Modulo', style=wx.ALIGN_CENTER)
        self.modulo_label.SetForegroundColour('#ffffff')
        self.modulo_label.SetFont(wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        col_izquierda_sizer = wx.BoxSizer(wx.VERTICAL)
        col_izquierda_sizer.AddStretchSpacer()
        col_izquierda_sizer.Add(self.modulo_label, flag=wx.ALIGN_CENTER)
        col_izquierda_sizer.AddStretchSpacer()

        col_izquierda.SetSizer(col_izquierda_sizer)
        sizer.Add(col_izquierda, pos=(0, 0), span=(2, 1), flag=wx.EXPAND|wx.ALL, border=0)

        # Columna derecha superior
        col_derecha_up = wx.Panel(panel)
        col_derecha_up.SetBackgroundColour('#614B79')

        self.descripcion_label = wx.StaticText(col_derecha_up, label='Descripción', style=wx.ALIGN_CENTER)
        self.descripcion_label.SetForegroundColour('#ffffff')
        self.descripcion_label.SetFont(wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
 
        col_derecha_up_sizer = wx.BoxSizer(wx.VERTICAL)
        col_derecha_up_sizer.AddStretchSpacer()
        col_derecha_up_sizer.Add(self.descripcion_label, flag=wx.ALIGN_CENTER)
        col_derecha_up_sizer.AddStretchSpacer()

        col_derecha_up.SetSizer(col_derecha_up_sizer)
        sizer.Add(col_derecha_up, pos=(0, 1), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=0)


        # Columna derecha inferior
        col_derecha_down = wx.Panel(panel)
        col_derecha_down.SetBackgroundColour('#ffffff')

        self.pin_label = wx.StaticText(col_derecha_down, label='Pin 1', style=wx.ALIGN_CENTER)
        self.pin_label.SetForegroundColour('#432D5C')
        self.pin_label.SetFont(wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        col_derecha_down_sizer = wx.BoxSizer(wx.VERTICAL)
        col_derecha_down_sizer.AddStretchSpacer()
        col_derecha_down_sizer.Add(self.pin_label, flag=wx.ALIGN_CENTER)
        col_derecha_down_sizer.AddStretchSpacer()

        col_derecha_down.SetSizer(col_derecha_down_sizer)
        sizer.Add(col_derecha_down, pos=(1, 1), flag=wx.EXPAND|wx.ALL, border=0)


        # Configurar la expansión del sizer
        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)

        panel.SetSizer(sizer)
        sizer.Fit(self)

        self.Show(True)

    def cambiar_texto(self):
        # Cambiar el texto de ejemplo
        self.modulo_label.SetLabel('Texto cambiado')

if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()
    