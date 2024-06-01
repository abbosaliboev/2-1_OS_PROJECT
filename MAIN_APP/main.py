# update 

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
import sys
import time
from plyer import vibrator 
import sqlite3
from kivy.properties import StringProperty, ListProperty

con=sqlite3.connect("mydatabase.db")
cur= con.cursor()

sys.path.append("./../yolo/yolov5/yolov5") # yolo 모델 사용을 위한 경로 추가
sys.path.append("./../src")

import detect # yolo의 detect 모듈 추가
import our_gTTS

product_name = None # 제품명을 저장하기 위한 변수

class MainScreen(Screen):
    def capture_image(self):
        global product_name
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
    
    #extract product data and send to .kv
    def set_product_name(self, product_name):
        self.load_product_data(product_name)

    def load_product_data(self, product_name):
        if product_name:
            cur.execute("SELECT * FROM product WHERE name = ?", (product_name,))
            product_data = cur.fetchone()    #데이터베이스로 부터 정보 받음
            if product_data:
                self.product_data = str(product_data)    #kv로 송출
            else:    #실패사례
                self.product_data = "Not Found"
        else:
            self.product_data = "No product detected."

    def add_to_basket(self):
        if product_name:
            self.basket.append(product_name)
            self.manager.get_screen('basket').update_basket(self.basket)
            
    def toggle_microphone(self):
        pass

class BasketScreen(Screen):
    class BasketScreen(Screen):
        basket_items = ListProperty([])

        def update_basket(self, items):
            self.basket_items = items
            self.ids.main_button.text = '\n'.join(self.basket_items)

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
