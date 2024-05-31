# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
import sys # 경로 추가를 위해
import time

#code to import database
import sqlite3
from kivy.properties import StringProperty
con=sqlite3.connect("product.db")
cur= con.cursor()

sys.path.append("./../yolo/yolov5/yolov5") # yolo 모델 사용을 위한 경로 추가
sys.path.append("./../src")

import detect # yolo의 detect 모듈 추가
import our_gTTS

product = None
# 제품명을 저장하기 위한 변수
class MainScreen(Screen):
    def capture_image(self):
        global product
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("photos/IMG.png".format(timestr))

        # yolo v5 사용부분
        opt = detect.parse_opt() # yolo의 작동을 위한 opt 받기
        result = detect.main(opt) # predict의 main 실행 => 제품과 확률의 쌍인 list가 리턴됨
        result = sorted(result,reverse=True,key=lambda x: x[1]) #확률을 기준으로 내림차순으로 정렬(다중 인식 처리를 위해)
        if not(result): # 어떤 제품도 인식 되지 않은 경우 product를 None으로(나중에 데이터 베이스에 맞게 활용)
            product = None
        else: # 제품이 있는 경우 리스트에서 제품 이름을 갖고와 제품명 출력
            product = result[0][0] # 가장 확률이 높은 아이템을 갖고오기
            print(product)
        ##### yolo에서 제품 추론 완료

        # tts 사용부분
        our_gTTS.main(product)
        # yolo로 제품명을 갖고 오는 것까지 구현완료 tts 구현, 알리가 프론트앤드 구현해줘야 함!
        
        

class SecondScreen(Screen):
    productdata=StringProperty(result)
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
