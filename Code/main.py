from pygrabber.dshow_graph import FilterGraph
from recognize import modules_recognizer,pin_recognizer
from dbms import data_manager
import cv2,wx,time,threading

def get_camera(name="HD camera ") :
    devices = FilterGraph().get_input_devices()
    for device_index, device_name in enumerate(devices):
        if device_name == name:
            return device_index
    return 0

class Controller:
    def __init__(self):
        try:             
            self.cap = cv2.VideoCapture(get_camera())     
            self.reconocedor_img = modules_recognizer()
            self.base_datos = data_manager()
        except Exception as e:
            print(e)

    def take_photo(self):
            _, frame = self.cap.read()
            frame = cv2.resize(frame, (224, 224))
            cv2.imshow('image',frame)
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            module_detected= self.reconocedor_img.read(rgb_frame)
            print('Detectado: ',module_detected)
#            module_name = self.base_datos.query_module(module_detected) #
            module_info = self.base_datos.query_module(module_detected) #
            return (module_detected,module_info)

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Blinduino',size=wx.GetDisplaySize())
        self.controller = Controller()
        self.pinsController = pin_recognizer()

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(hgap=0, vgap=0)

        # Columna izquierda superior
        self.col_izquierda_up = wx.Panel(panel, name="Modulo")
        self.col_izquierda_up.SetBackgroundColour('#432D5C')

        self.modulo_label = wx.StaticText(self.col_izquierda_up, label='Modulo', style=wx.ALIGN_CENTER)
        self.modulo_label.SetForegroundColour('#ffffff')
        self.modulo_label.SetFont(wx.Font(40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        col_izquierda_up_sizer = wx.BoxSizer(wx.VERTICAL)
        col_izquierda_up_sizer.AddStretchSpacer()
        col_izquierda_up_sizer.Add(self.modulo_label, flag=wx.ALIGN_CENTER)
        col_izquierda_up_sizer.AddStretchSpacer()

        self.col_izquierda_up.SetSizer(col_izquierda_up_sizer)
        sizer.Add(self.col_izquierda_up, pos=(0, 0), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=0)

        # Columna izquierda inferior
        self.col_izquierda_down = wx.Panel(panel,name="Pin 1")
        self.col_izquierda_down.SetBackgroundColour('#ffffff')

        self.pin_label = wx.StaticText(self.col_izquierda_down, label='Pin 1', style=wx.ALIGN_CENTER)
        self.pin_label.SetForegroundColour('#432D5C')
        self.pin_label.SetFont(wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        col_izquierda_down_sizer = wx.BoxSizer(wx.VERTICAL)
        col_izquierda_down_sizer.AddStretchSpacer()
        col_izquierda_down_sizer.Add(self.pin_label, flag=wx.ALIGN_CENTER)
        col_izquierda_down_sizer.AddStretchSpacer()

        self.col_izquierda_down.SetSizer(col_izquierda_down_sizer)
        sizer.Add(self.col_izquierda_down, pos=(1, 0), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=0)

        # Columna derecha superior
        self.col_derecha_up = wx.Panel(panel,name="Descripción")
        self.col_derecha_up.SetBackgroundColour('#614B79')

        self.descripcion_label = wx.StaticText(self.col_derecha_up, label='Descripción', style=wx.ALIGN_CENTER)
        self.descripcion_label.SetForegroundColour('#ffffff')
        self.descripcion_label.SetFont(wx.Font(35, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        col_derecha_up_sizer = wx.BoxSizer(wx.VERTICAL)
        col_derecha_up_sizer.AddStretchSpacer()
        col_derecha_up_sizer.Add(self.descripcion_label, flag=wx.ALIGN_CENTER)
        col_derecha_up_sizer.AddStretchSpacer()

        self.col_derecha_up.SetSizer(col_derecha_up_sizer)
        sizer.Add(self.col_derecha_up, pos=(0, 1), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=0)

        # Columna derecha inferior
        self.col_derecha_down = wx.Panel(panel,name="DETECTAR")
        self.col_derecha_down.SetBackgroundColour('#ffffff')

        self.boton_detect = wx.Button(self.col_derecha_down, label='DETECTAR')
        self.boton_detect.SetHelpText("Este botón se usa para tomar una foto e identificar el modulo")
        self.boton_detect.SetForegroundColour('#ffffff')
        self.boton_detect.SetBackgroundColour('#614B79')
        self.boton_detect.SetFont(wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.boton_detect.Bind(wx.EVT_BUTTON, self.cambiar_texto)


        col_derecha_down_sizer = wx.BoxSizer(wx.VERTICAL)
        col_derecha_down_sizer.AddStretchSpacer()
        col_derecha_down_sizer.Add(self.boton_detect, flag=wx.ALIGN_CENTER)
        col_derecha_down_sizer.AddStretchSpacer()

        self.col_derecha_down.SetSizer(col_derecha_down_sizer)
        sizer.Add(self.col_derecha_down, pos=(1, 1), flag=wx.EXPAND|wx.ALL, border=0)


        # Configurar la expansión del sizer
        sizer.AddGrowableCol(0,4)
        sizer.AddGrowableCol(1,6)
        sizer.AddGrowableRow(0)
        sizer.AddGrowableRow(1)

        panel.SetSizer(sizer)
#        sizer.Fit(self)
        self.SetMinSize((800, 600))
        self.Show(True)

        self.thread = threading.Thread(target=self.update_pin_label)
        self.thread.start()

    def cambiar_texto(self,event):
        nombre_modulo,info_modulo = self.controller.take_photo()
        
        width_modulo = self.modulo_label.GetParent().GetSize()[0]
        self.col_izquierda_up.SetLabel(nombre_modulo)
        self.modulo_label.SetLabel(nombre_modulo)
        self.modulo_label.Wrap(width_modulo)
        self.modulo_label.GetParent().Layout()

        width_description = self.descripcion_label.GetParent().GetSize()[0]
        self.col_derecha_up.SetLabel(info_modulo)
        self.descripcion_label.SetLabel(info_modulo)
        self.descripcion_label.Wrap(width_description)
        self.descripcion_label.GetParent().Layout()

    def update_pin_label(self):
        if self.pinsController.gamepad:
            while True:
                time.sleep(1)
                report = self.pinsController.gamepad.read(64)
                if report and report[1] in self.pinsControllerself.nombre_pin.keys():
                    wx.CallAfter(self.pin_label.SetLabel, self.pinsControllerself.nombre_pin[report[1]])
                    wx.CallAfter(self.col_izquierda_down.SetLabel, self.pinsControllerself.nombre_pin[report[1]])

if __name__ == '__main__':
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()
    