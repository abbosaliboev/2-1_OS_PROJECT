# main.py
import kivy
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

kivy.require('2.3.0')  # 현재 사용하는 Kivy 버전

class CameraApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')  # 레이아웃 객체 생성
        self.camera = Camera(play=False)  # 카메라 객체 생성, 초기 상태는 꺼짐
        layout.add_widget(self.camera)  # 카메라 위젯을 레이아웃에 추가

        # 카메라를 켜고 끄는 버튼 추가
        button = Button(text='Toggle Camera', size_hint=(1, 0.2),
                        on_press=self.toggle_camera)
        layout.add_widget(button)

        return layout

    def toggle_camera(self, *args):
        self.camera.play = not self.camera.play  # 카메라 상태 토글

if __name__ == '__main__':
    CameraApp().run()