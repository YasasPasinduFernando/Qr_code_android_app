from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
import qrcode
from PIL import Image as PILImage
import os

class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent
        self.color = get_color_from_hex('#FFFFFF')
        self.font_size = '16sp'
        self.bold = True
        
        # Custom background
        with self.canvas.before:
            Color(0.2, 0.6, 0.86, 1)  # Bright blue color
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        
        # Bind position and size updates
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class QRCodeApp(App):
    def build(self):
        # Set window properties
        Window.size = (350, 600)
        Window.clearcolor = get_color_from_hex('#F0F4F8')  # Light blue-gray background
        
        # Main layout
        self.layout = BoxLayout(
            orientation="vertical", 
            padding=20, 
            spacing=15
        )
        
        # Title Label
        title = Label(
            text="QR Code Generator", 
            font_size='24sp', 
            color=get_color_from_hex('#2C3E50'),
            bold=True
        )
        self.layout.add_widget(title)
        
        # Data Input
        input_layout = BoxLayout(orientation='vertical', spacing=5)
        input_label = Label(
            text="Enter Data:", 
            halign='left', 
            color=get_color_from_hex('#34495E'),
            size_hint_y=None, 
            height=30
        )
        self.input = TextInput(
            multiline=False, 
            size_hint=(1, None), 
            height=50,
            background_color=get_color_from_hex('#FFFFFF'),
            foreground_color=get_color_from_hex('#2C3E50'),
            padding=[10, 10]
        )
        input_layout.add_widget(input_label)
        input_layout.add_widget(self.input)
        self.layout.add_widget(input_layout)
        
        # QR Code Color Spinner
        color_layout = BoxLayout(spacing=10)
        color_label = Label(
            text="QR Code Color:", 
            color=get_color_from_hex('#34495E'),
            size_hint_x=0.4
        )
        self.color_spinner = Spinner(
            text='Black',
            values=('Black', 'Blue', 'Green', 'Red', 'Purple'),
            size_hint=(0.6, None),
            height=50
        )
        color_layout.add_widget(color_label)
        color_layout.add_widget(self.color_spinner)
        self.layout.add_widget(color_layout)
        
        # Generate Button
        self.generate_btn = StyledButton(
            text="Generate QR Code", 
            size_hint=(1, None), 
            height=50
        )
        self.generate_btn.bind(on_press=self.generate_qrcode)
        self.layout.add_widget(self.generate_btn)
        
        # QR Code Image
        self.qr_image = Image(
            size_hint=(1, 0.6), 
            allow_stretch=True
        )
        self.layout.add_widget(self.qr_image)
        
        # Status Label
        self.status_label = Label(
            text="", 
            color=get_color_from_hex('#E74C3C'),
            font_size='14sp'
        )
        self.layout.add_widget(self.status_label)
        
        return self.layout

    def generate_qrcode(self, instance):
        data = self.input.text.strip()
        if not data:
            self.status_label.text = "Please enter valid data!"
            return

        # Color mapping
        color_map = {
            'Black': 'black',
            'Blue': 'blue',
            'Green': 'green',
            'Red': 'red',
            'Purple': 'purple'
        }
        fill_color = color_map.get(self.color_spinner.text, 'black')

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1, 
            box_size=10, 
            border=4,
            error_correction=qrcode.constants.ERROR_CORRECT_L
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color=fill_color, 
            back_color="white"
        )
        
        # Save QR Code
        img_path = os.path.join(os.getcwd(), "generated_qrcode.png")
        img.save(img_path)

        # Show QR Code
        self.qr_image.source = img_path
        self.qr_image.reload()
        
        # Update status
        self.status_label.text = "QR Code Generated Successfully!"

if __name__ == "__main__":
    QRCodeApp().run()