from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button

class RootWidget(BoxLayout):
    def toggle_microphone(self):
        # Mikrofonni yoqish/ochish logikasini qo'shing
        pass

class MyApp(App):
    def build(self):
        root = RootWidget()
        root.ids.camera.play = True  # Kamera avtomatik ravishda ochiladi
        return root

if __name__ == '__main__':
    MyApp().run()
