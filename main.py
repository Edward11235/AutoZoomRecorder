from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from pynput import mouse
import pyautogui
from database import DataBase


Builder.load_file("my.kv")


class MainWindow(Screen):
    zoomid = ObjectProperty(None)
    zoompassword = ObjectProperty(None)
    meetingid = ObjectProperty(None)
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


db = DataBase("info.txt")

class AutoZoomRecorderApp(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    AutoZoomRecorderApp().run()