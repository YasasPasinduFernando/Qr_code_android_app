from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.label import Label
import qrcode
from PIL import Image as PILImage
import os

class QRCodeApp(App):
    def build(self):
        Window.size = (500, 650)
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        self.label = Label(text="Enter Data for QR Code:")
        self.layout.add_widget(self.label)

        self.input = TextInput(multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.input)

        self.generate_btn = Button(text="Generate QR Code", size_hint=(1, 0.1))
        self.generate_btn.bind(on_press=self.generate_qrcode)
        self.layout.add_widget(self.generate_btn)

        self.qr_image = Image(size_hint=(1, 0.6))
        self.layout.add_widget(self.qr_image)

        return self.layout

    def generate_qrcode(self, instance):
        data = self.input.text.strip()
        if not data:
            self.label.text = "Please enter valid data!"
            return

        # Generate QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = os.path.join(os.getcwd(), "qrcode.png")
        img.save(img_path)

        # Show QR Code
        self.qr_image.source = img_path
        self.qr_image.reload()
        self.label.text = "QR Code Generated Successfully!"

if __name__ == "__main__":
    QRCodeApp().run()

