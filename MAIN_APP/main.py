#import camera code
# !!! This is temporary!!!         --> file path must be defined for use in YOLO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from plyer import camera
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import os

class CameraApp(App):
    def build(self):
        self.img = Image()
        
        layout = BoxLayout(orientation='vertical')
        
        btn_take_photo = Button(text='Take Photo', size_hint=(1, 0.2))
        btn_take_photo.bind(on_press=self.take_photo)
        
        layout.add_widget(self.img)
        layout.add_widget(btn_take_photo)
        
        return layout

    def take_photo(self, instance):
        try:
            # Define the file path where the photo will be saved
            file_path = os.path.join(self.user_data_dir, 'photo.png')
            
            # Take a photo and save it to the specified location
            camera.take_picture(file_path, self.on_picture_taken)
        except Exception as e:
            popup = Popup(title='Error',
                          content=Label(text=str(e)),
                          size_hint=(0.8, 0.8))
            popup.open()
    
    def on_picture_taken(self, file_path):
        if os.path.exists(file_path):
            # Display the photo in the app
            self.img.source = file_path
            self.img.reload()
        else:
            popup = Popup(title='Error',
                          content=Label(text='Failed to save photo.'),
                          size_hint=(0.8, 0.8))
            popup.open()

if __name__ == '__main__':
    CameraApp().run()

#send picture to yolo

#extract product name

#find name from database
cur.execute("SELECT * FROM product WHERE name=?", (result[0],))
result = cur.fetchone()
print("\nfrom product:")
print(result[0])    #name
print(result[1])    #brand company
print(result[2])    #price
print(result[3])    #capacity
print(result[4])    #calorie

#con.close()

#show on screen

#other features
