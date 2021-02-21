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
import time
from private_info import SUDO_PASSWORD

Builder.load_file("my.kv")

class MainWindow(Screen):
    zoomid = ObjectProperty(None)
    zoompassword = ObjectProperty(None)
    meetingid = ObjectProperty(None)
    start_time = ObjectProperty(None)
    end_time = ObjectProperty(None)
    test = ObjectProperty(None)
    startapp = ObjectProperty(None)
    time_to_start = -1
    duration = -1
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

    def add_user(self):
        userid = self.zoomid.text
        password = self.zoompassword.text
        meetingid = self.meetingid.text
        userdb.add_user(userid, password, meetingid)

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
        if self.time_to_start > 0 and self.duration > 0:
            # temp_hour = self.time_to_start // 60
            # temp_min = self.time_to_start % 60
            # self.startapp.text = "Testing is going to start in %dhour %dmin" % (temp_hour, temp_min)
            self.countDown()

    def countDown(self):
        self.sec = 59
        def update_label(*largs):
            temp_hour = self.time_to_start // 60
            temp_min = self.time_to_start % 60
            self.startapp.text = "Meeting is going to start in %dhour %dmin " \
                                 "%dsec" % (temp_hour, temp_min, self.sec)
            self.sec = self.sec - 1
            if self.sec == -1:
                self.time_to_start -= 1
                self.sec = 59

            if self.time_to_start == 0:
                self.func_interval.cancel()
                self.start()

        self.func_interval = Clock.schedule_interval(update_label, 1)

    def testCountDonw(self):
        self.temp_sec = 5
        def test_update_label(*largs):
            self.test.text = "Testing is going to start in %d sec" % (self.temp_sec)
            self.temp_sec -= 1
            if self.temp_sec == -1:
                self.test.text = "Testing has been initiated"
                self.func_interval_test.cancel()
                self.start()

        self.func_interval_test = Clock.schedule_interval(test_update_label, 1)

    def start(self):
        self.add_user()
        self.routines()

    def click_something(self, buttonname):
        temp1, temp2 = db.btnlist[buttonname]
        temp1, temp2 = float(temp1), float(temp2)
        pyautogui.click(temp1, temp2)

    def stable_hotkey(self, key1, key2):
        pyautogui.keyDown(key1)
        pyautogui.keyDown(key2)
        pyautogui.keyUp(key2)
        pyautogui.keyUp(key1)

    def stable_three_hotkey(self, key1, key2, key3):
        pyautogui.keyDown(key1)
        pyautogui.keyDown(key2)
        pyautogui.keyDown(key3)
        pyautogui.keyUp(key3)
        pyautogui.keyUp(key2)
        pyautogui.keyUp(key1)

    def routines(self):
        self.stable_hotkey('command', 'space')
        pyautogui.typewrite("zoom.us")
        pyautogui.typewrite(["enter"])
        time.sleep(1)
        self.click_something('SignIn1')
        pyautogui.typewrite(self.zoomid.text)
        self.click_something('Password')
        pyautogui.typewrite(self.zoompassword.text)
        self.click_something('KeepMe')
        self.click_something('SignIn2')
        time.sleep(5)
        self.stable_hotkey('command', 'j')
        self.click_something('MeetID')
        if ':' in self.meetingid.text:
            idmeeting = self.meetingid.text.split(':')[0]
            passmeeting = self.meetingid.text.split(':')[1]
            pyautogui.typewrite(idmeeting)
            # self.click_something('NoAudio')
            self.click_something('Join')
            time.sleep(5)
            pyautogui.typewrite(passmeeting)
            pyautogui.press('enter')
        else:
            pyautogui.typewrite(self.meetingid.text)
            # self.click_something('NoAudio')
            self.click_something('Join')
        time.sleep(20)
        self.click_something('Audio')
        self.click_something('Auto')
        self.click_something('PCAudio')
        self.stable_three_hotkey('command', 'shift', '5')
        self.click_something('Recording')
        pyautogui.typewrite(["enter"])
        print(self.duration)
        if self.duration == -1:
            print('a')
            # Clock.schedule_once(self.finish, 30)
            time.sleep(20)
            self.finish()
            time.sleep(10)
            self.shutdonw()
        else:
            time.sleep(60*self.duration)
            self.finish()
            time.sleep(60)
            self.shutdonw()

    def finish(self, *largs):
        print(1)
        self.stable_three_hotkey('command', 'ctrl', 'esc')
        self.stable_hotkey('command', 'q')

    def shutdonw(self, *largs):
        self.stable_hotkey('command', 'space')
        pyautogui.typewrite('terminal')
        pyautogui.typewrite(["enter"])
        time.sleep(3)
        pyautogui.typewrite('sudo shutdown -h now')
        pyautogui.typewrite(["enter"])
        pyautogui.typewrite(SUDO_PASSWORD)
        pyautogui.typewrite(["enter"])

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
