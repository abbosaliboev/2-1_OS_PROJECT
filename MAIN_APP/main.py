#update
import sys
import time
import sqlite3

from plyer import vibrator
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout


# Register NanumGothicBold.ttf as the default font for proper Korean text display
LabelBase.register(DEFAULT_FONT, 'NanumGothicBold.ttf')

# Connect to SQLite database
con = sqlite3.connect("mydatabase.db")
cur = con.cursor()

# Add paths for yolo model usage
sys.path.append("./../yolo/yolov5/yolov5")
sys.path.append("./../src")

# Import yolo's detect module and our_gTTS for text-to-speech conversion
import detect
import our_gTTS

# Variable to store product name
product_name = None

class MainScreen(Screen):
    # Method to capture image from camera
    def capture_image(self):
        global product_name  # Use global variable
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("photos/IMG.png".format(timestr))

        # Use yolo v5 for object detection
        opt = detect.parse_opt()
        result = detect.main(opt)  # Run detection and get result as list of (product, probability)
        result = sorted(result, reverse=True, key=lambda x: x[1])  # Sort by probability in descending order
        if not result:  # If no product detected
            product_name = None
        else:  # If products detected, take the one with highest probability
            product_name = result[0][0]
            print(product_name)

        # Use text-to-speech to announce the detected product
        our_gTTS.main(product_name, 0)

        # Store product_name in the app instance for use in other screens
        self.manager.get_screen('second').set_product_name(product_name)

        # Change screen only if product_name is not None
        if product_name is not None:
            self.manager.current = 'second'

class SecondScreen(Screen):
    # Properties to hold product data, basket items, and total price
    product_data = StringProperty('')
    basket = ListProperty([])
    price = NumericProperty(0)

    # Method to set product name and load its data
    def set_product_name(self, product_name):
        self.load_product_data(product_name)

    # Method to load product data from the database
    def load_product_data(self, product_name):
        if product_name:
            cur.execute("SELECT * FROM products WHERE name = ?", (product_name,))
            product_data = cur.fetchone()  # Fetch product data from database
            if product_data:
                # Extract product details and update properties
                self.product_name = str(product_data[3])
                self.product_brand = str(product_data[2])
                self.product_price = str(product_data[4])
                self.product_capacity = str(product_data[5])
                self.product_calorie = str(product_data[6])
                self.product_data = f"이름: {self.product_name}\n\n {self.product_brand}\n가격: {self.product_price}\n용량: {self.product_capacity}\n칼로리: {self.product_calorie}"
            else:  # If product not found in database
                self.product_data = "Not Found"
        else:
            self.product_data = "No product detected."

    # Method to add product to basket
    def add_to_basket(self):
        global product_name  # Use global variable to get product name
        if product_name:
            cur.execute("SELECT price FROM products WHERE name = ?", (product_name,))
            price = cur.fetchone()[0]
            self.basket.append((product_name, price))  # Add product to basket
            self.manager.get_screen('basket').update_basket(self.basket)  # Update basket screen

    # Method to trigger TTS for the detected product
    def announce_product(self):
        if product_name:
            our_gTTS.main(product_name, 1)

class BasketScreen(Screen):
    # Properties to hold basket items and total price
    basket_items = ListProperty([])
    total_price = NumericProperty(0)
    basket_list = StringProperty("")
    total_price_text = StringProperty("")
    item_counts = {}  # Dictionary to hold item counts

    # Method to update basket items and total price
    def update_basket(self, items):
        # Reset basket items and item counts
        self.basket_items = []
        self.item_counts = {}

        # Update basket items and calculate item counts
        for item in items:
            product_name, price = item
            if product_name in self.item_counts:
                self.item_counts[product_name]['count'] += 1
            else:
                self.item_counts[product_name] = {'count': 1, 'price': price}
            self.basket_items.append(item)

        # Calculate total price
        self.total_price = sum([item[1] for item in items])

        # Update the UI with basket items and total price
        self.update_ui()

    # Method to clear basket and reset total price
    def reset_basket(self):
        self.basket_items = []
        self.total_price = 0
        self.item_counts = {}  # Reset item counts
        self.update_ui()

    # Update UI with current basket items and total price
    def update_ui(self):
        if not self.basket_items:
            self.basket_list = "So empty...\nBuy something!"
            self.total_price_text = "Total Price: ₩0"
        else:
            basket_string = "\n\n"
            for product_name, info in self.item_counts.items():
                basket_string += f"{product_name}: ₩{int(info['price'])}\t x {info['count']}\n"

            self.basket_list = basket_string
            self.total_price_text = f"Total: ₩{self.total_price}"

    def announce_basket(self):
        if not self.basket_items:
            # Basket is empty, announce that
            tts_text = "장바구니가 비어있습니다."
        else:
            # Prepare text for TTS
            basket_items_str = ', '.join([f"{name} {info['count']}개" for name, info in self.item_counts.items()])
            tts_text = f"장바구니에는 {basket_items_str}가 있습니다. 총 가격은 {self.total_price}원입니다."
        our_gTTS.announce_basket_info(tts_text)

class PayScreen(Screen):
    pass

class SettingScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        # Create the screen manager and add all screens
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(BasketScreen(name='basket'))
        sm.add_widget(PayScreen(name='pay'))
        sm.add_widget(SettingScreen(name='setting'))
        return sm

if __name__ == '__main__':
    MyApp().run()
