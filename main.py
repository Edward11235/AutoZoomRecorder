from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from pynput import mouse

Builder.load_file("my.kv")

def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
    else:
        print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))
    if not pressed:
        return False # Stop listener

class MyGrid(Widget):  #MyGrid首先继承了GridLayout.在其中又声明了一个新的GridLayout对象
    name = ObjectProperty(None)  #when nothing is read, use None
    email = ObjectProperty(None)

    def btn(self):
        #print(pyautogui.position())
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        listener.join()
        print("Name:", self.name.text, "email:", self.email.text,  )

class AutoZoomRecorderApp(App):
    def build(self):
        return FloatLayout()

if __name__ == "__main__":
    AutoZoomRecorderApp().run()