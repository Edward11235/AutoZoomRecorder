from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from pynput import mouse
import pyautogui


Builder.load_file("my.kv")


class MainWindow(Screen):
    zoomid = ObjectProperty(None)
    zoompassword = ObjectProperty(None)
    meetingid = ObjectProperty(None)
    temp_x = temp_y = -1.0

    def on_click(self, x, y, button, pressed):
        if button == mouse.Button.left:
            print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
            self.temp_x = float(x)
            self.temp_x = float(x)
        else:
            print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))
        if not pressed:
            return False  # Stop listener

    def add_position(self):
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()
        listener.join()
        # 把temp_x和temp_y存入数据库中


class AutoZoomRecorderApp(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    AutoZoomRecorderApp().run()