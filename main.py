from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from pynput import mouse
import pyautogui
from database import DataBase
import datetime
from kivy.clock import Clock
from functools import partial


Builder.load_file("my.kv")


class MainWindow(Screen):
    zoomid = ObjectProperty(None)
    zoompassword = ObjectProperty(None)
    meetingid = ObjectProperty(None)
    start_time = ObjectProperty(None)
    end_time = ObjectProperty(None)
    test = ObjectProperty(None)
    startapp = ObjectProperty(None)
    time_to_start = duration = -1
    temp_x = temp_y = -1.0  #用于存储读取的点击位置的坐标

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
            self.temp_x = float(x)
            self.temp_y = float(y)
        else:
            print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))
        if not pressed:
            return False  # Stop listener

    def add_position(self, btn_name):
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()
        listener.join()
        # 把btn_name以及对应的temp_x和temp_y存入数据库中
        if isinstance(self.temp_x, float) and isinstance(self.temp_x, float) and isinstance(btn_name, str):
            db.add_pos(btn_name, self.temp_x, self.temp_y)

    # def test(self):
    #     self.start(start=now+60)

    def initialize(self):
        try:
            a, b = self.start_time.text.split(":")
            c, d = self.end_time.text.split(":")
            self.time_to_start = (int(a) - datetime.datetime.now().hour) * 60 + int(b) - datetime.datetime.now().minute
            self.duration = (int(c) - int(a))*60 + int(d) - int(b)
            if self.time_to_start < 0 or self.duration < 0:
                raise Exception()
            if self.duration == -1 or self.time_to_start == -1:
                raise Exception()
        except:
            #popup
            print("时间格式错误")
        if self.duration > 60:
            #popup
            print("popup:超出时间上限（60分钟)")
        elif self.time_to_start > 0 and self.duration > 0:
            temp_hour = self.time_to_start // 60
            temp_min = self.time_to_start % 60
            self.startapp.text = "Testing is going to start in %dhour %dmin" % (temp_hour, temp_min)
            self.countDown()


    def countDown(self):

        def update_label(*largs):
            temp_hour = self.time_to_start // 60
            temp_min = self.time_to_start % 60
            self.startapp.text = "Testing is going to start in %dhour %dmin" % (temp_hour, temp_min)
            self.time_to_start -= 1
            if self.time_to_start == 0:
                self.start()
                self.func_interval.cancel()

        self.func_interval = Clock.schedule_interval(partial(update_label), 60)

    def testDountDonw(self):
        pass

    def start(self):
        print("1")

db = DataBase("info.txt")
userdb = DataBase("user.txt")


class AutoZoomRecorderApp(App):
    def build(self):
        MW = MainWindow()
        MW.zoomid.text = userdb.zoomid
        MW.zoompassword.text = userdb.zoompassword
        MW.meetingid.text = userdb.meetingid
        return MW

if __name__ == "__main__":
    AutoZoomRecorderApp().run()