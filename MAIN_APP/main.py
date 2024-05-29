# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
import time

import sqlite3
con=sqlite3.connect("product.db")
cur con.cursor()


class MainScreen(Screen):
    def capture_image(self):
        camera = self.ids['camera']
        camera.export_to_png("photos/IMG.png")
        print("Captured")

#Yolo access IMG/png from photo file
#save name to "name"

#find referring product in database and save info to result
cur.execute("SELECT * FROM product WHERE name=Cocacola", (result[0],))
result = cur.fetchone()

class SecondScreen(Screen):
    productdata=Stringproperty(result)
    def toggle_microphone(self):
        # Add logic for enabling/disabling the microphone here
        pass

class SettingScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(SettingScreen(name='setting'))
        return sm


if __name__ == '__main__':
    MyApp().run()
