from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
import time
from plyer import vibrator 
import sqlite3

# Database connection
con = sqlite3.connect("temp.db")
cur = con.cursor()

# Create the necessary tables if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS product
               (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')

# Assuming you have some initial data to insert into the product table
cur.execute('''INSERT INTO product (name, price) VALUES (?, ?)''', ('Product1', 10.0))
con.commit()

class MainScreen(Screen):
    def capture_image(self):
        camera = self.ids['camera']
        camera.export_to_png("photos/IMG.png")
        print("Captured")
        # self.vibrate_device()  

    def vibrate_device(self):
        vibrator.vibrate(time=0.1)  

    def get_product_name(self):
        # Fetch product name from the database
        con = sqlite3.connect("temp.db")
        cur = con.cursor()
        cur.execute("SELECT name FROM product")
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return "No Product Found"  # Default text if no product is found
        
class SecondScreen(Screen):
    def toggle_microphone(self):
        
        pass

class BasketScreen(Screen):
    pass

class PayScreen(Screen):
    pass

class SettingScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(BasketScreen(name='basket'))
        sm.add_widget(PayScreen(name='pay'))
        sm.add_widget(SettingScreen(name='setting'))
        return sm

if __name__ == '__main__':
    MyApp().run()
