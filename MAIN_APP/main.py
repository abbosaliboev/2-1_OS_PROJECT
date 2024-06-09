from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.text import LabelBase, DEFAULT_FONT
import sys
import time
from plyer import vibrator 
import sqlite3
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout


# 한국어의 정상적인 출력을 위해서 기본 폰트를 'NanumGothicBold.ttf'로 설정함.
LabelBase.register(DEFAULT_FONT, 'NanumGothicBold.ttf')

con=sqlite3.connect("mydatabase.db")
cur= con.cursor()

sys.path.append("./../yolo/yolov5/yolov5") # yolo 모델 사용을 위한 경로 추가
sys.path.append("./../src")

import detect # yolo의 detect 모듈 추가
import our_gTTS   # 텍스트를 음성으로 변환하는 our_gTTS 모듈 임포트


product_name = None # 제품명을 저장하기 위한 변수



class MainScreen(Screen):
    def capture_image(self):
        global product_name    #전역변수 사용
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("photos/IMG.png".format(timestr))

        # yolo v5 사용부분
        opt = detect.parse_opt() # yolo의 작동을 위한 opt 받기
        result = detect.main(opt) # predict의 main 실행 => 제품과 확률의 쌍인 list가 리턴됨
        result = sorted(result,reverse=True,key=lambda x: x[1]) #확률을 기준으로 내림차순으로 정렬(다중 인식 처리를 위해)
        if not(result): # 어떤 제품도 인식 되지 않은 경우 product를 None으로(나중에 데이터 베이스에 맞게 활용)
            product_name = None
        else: # 제품이 있는 경우 리스트에서 제품 이름을 갖고와 제품명 출력
            product_name = result[0][0] # 가장 확률이 높은 아이템을 갖고오기
            print(product_name)
        ##### yolo에서 제품 추론 완료

        # tts 사용부분
        our_gTTS.main(product_name)
        # yolo로 제품명을 갖고 오는 것까지 구현완료 tts 구현, 알리가 프론트앤드 구현해줘야 함!
    
        # Store product_name in the app instance
        self.manager.get_screen('second').set_product_name(product_name)
        
        
class SecondScreen(Screen):
    
    product_data=StringProperty('')
    basket = ListProperty([])    #장바구니 리스트
    price = NumericProperty(0)
    
    #extract product data and send to .kv
    def set_product_name(self, product_name):
        self.load_product_data(product_name)

    def load_product_data(self, product_name):
        if product_name:
            cur.execute("SELECT * FROM products WHERE name = ?", (product_name,))
            product_data = cur.fetchone()    #데이터베이스로 부터 정보 받음
            if product_data:
                self.product_name = str(product_data[3])  #kv로 송출
                self.product_brand = str(product_data[2])
                self.product_price = str(product_data[4])
                self.product_capacity = str(product_data[5])
                self.product_calorie = str(product_data[6])
                self.product_data = f"이름: {self.product_name}\n {self.product_brand}\n가격: {self.product_price}\n용량: {self.product_capacity}\n칼로리: {self.product_calorie}"

            else:    #실패사례
                self.product_data = "Not Found"
        else:
            self.product_data = "No product detected."

    def add_to_basket(self):
        global product_name_global  # Use global variable to get product name
        if product_name_global:
            cur.execute("SELECT price FROM products WHERE name = ?", (product_name_global,))
            price = cur.fetchone()[0]
            self.basket.append((product_name_global, price))  # Add product to basket
            self.manager.get_screen('basket').update_basket(self.basket)  # Update basket screen
            
    def toggle_microphone(self):
        pass

class BasketScreen(Screen):
    basket_items = ListProperty([])  # List property to hold basket items
    total_price = NumericProperty(0)  # Property to hold total price
    total_price_text = StringProperty("")  # Property to hold text for total price and items

    def update_basket(self, items):
        self.basket_items = items  # Update basket items
        self.total_price = sum([item[1] for item in items])  # Calculate total price
        self.total_price_text = f"Total Price: ${self.total_price:.2f}\nItems:\n" + "\n".join([f"{item[0]}: ${item[1]:.2f}" for item in items])  # Update text property
        
        self.ids.basket_grid.clear_widgets()  # Clear existing widgets
        for item in self.basket_items:
            label = Label(text=f"{item[0]}: ${item[1]:.2f}", size_hint_y=None, height=40)
            self.ids.basket_grid.add_widget(label)  # Add item labels to the grid layout
        # Update the total price label
        self.ids.price_label.text = f"Total Price: ${self.total_price:.2f}"

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
