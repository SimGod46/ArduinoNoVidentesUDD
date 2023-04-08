from pygrabber.dshow_graph import FilterGraph
import threading,cv2

class camera:
    def __init__(self,camera_name="HD Camera "):

        self.graph = FilterGraph()
        device_list = self.graph.get_input_devices()
        camera_indx = next(device[0] for device in enumerate(device_list) if device[1] == camera_name)

        self.graph.add_video_input_device(camera_indx)
        self.graph.add_sample_grabber(self.img_cb)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()

        self.image_done = threading.Event()
        self.image_grabbed = None
    def img_cb(self,image):
        self.image_grabbed = image
        self.image_done.set()

    def capture(self):
        self.graph.grab_frame()
        self.image_done.wait(1000)
        self.image_done.clear()
        frame = cv2.resize(self.image_grabbed, (224, 224))
#        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('image',frame)
        return frame
