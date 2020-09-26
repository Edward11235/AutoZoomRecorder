from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from pynput import mouse

Builder.load_file("my.kv")


def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
    else:
        print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))
    if not pressed:
        return False # Stop listener

class MainWindow(Screen):
    zoomid = ObjectProperty(None)
    zoompassword = ObjectProperty(None)
    meetingid = ObjectProperty(None)

    def position(self):
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        listener.join()

class AutoZoomRecorderApp(App):
    def build(self):
        return MainWindow()

if __name__ == "__main__":
    AutoZoomRecorderApp().run()