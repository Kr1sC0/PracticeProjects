from pyzbar.pyzbar import decode
import re
import qrcode  
from PIL import Image

class QRCodeGenerator:
    def __init__(self, version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4) -> None:
        self.qr = qrcode.QRCode(version=version, 
                                error_correction=error_correction, 
                                box_size=box_size, 
                                border=border)
    def add_data(self, data):
        """Add data to QRCode"""
        self.qr.add_data(data)
        self.qr.make(fit=True)
    def generate_image(self, fill_color='black', back_color='white'):
        """Generate QR Code image"""
        img = self.qr.make_image(fill=fill_color, back_color=back_color)
        return img
    def save_image(self, imgname, fill_color='black', back_color='white'):
        """Save image as specified name"""
        img = self.generate_image(fill_color, back_color)
        img.save(imgname)

def main():
    # All functionality logic goes here
    while True:
        func_num = input('1. Text to QR code.\n2. Decode QR code image\n3. Display QR code\n4. Generate multiple QR codes\nSelect an option: ').strip()
        if func_num not in ['1', '2', '3', '4']:
            print("Please make a valid entry")
        elif func_num == '1':
            link = input("Please enter a link: ")
            filename = input("Please enter desired filename: ")
            text_to_qr(valid_url(link), filename)
        elif func_num == '2':
            image_path = input("Please input path to QR code image to decode: ")
            decoded_text = decode_img(image_path)
            print(f"Decoded text: {decoded_text}")
        elif func_num == '3':
            link = input("Please enter a link to generate a QR code: ")
            img = QRCodeGenerator().generate_image(valid_url(link))
            display_qr_image(img)
        elif func_num == '4':
            list_of_links = input("Enter a list of links separated by commas: ").split(',')
            filenames = input("Enter corresponding filenames separated by commas: ").split(',')
            generate_multiple_qrcodes(list_of_links, filenames)
        break

def valid_url(link: str):
    pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(:[0-9]{1,5})?(\/.*)?$')
    if re.match(pattern, link):
        return link
    else:
        print("Invalid link. Please try again.")
        return ""

def display_qr_image(qr_image) -> None:
    """Display the QR code image."""
    qr_image.show()

def text_to_qr(text: str, filename: str) -> None:
    generator = QRCodeGenerator()
    generator.add_data(text)
    if filename:
        generator.save_image(filename)
    return generator.generate_image()

def decode_img(image_path: str) -> str:
    """Decode img contained in a QR code"""
    img = Image.open(image_path)
    decode_objects = decode(img)
    for obj in decode_objects:
        return obj.data.decode('utf-8')

def generate_multiple_qrcodes(list_of_links: str, filenames: str) -> None:
    # ValueError raised if the list of links are not equal to the amount of output filenames
    if len(list_of_links) != len(filenames):
        raise ValueError("List of names and filenames must have the same number of elements")
    # Loops through the list of names and file namesand generates/saves qr codes
    for name, filename in zip(list_of_links, filenames):
        generator = QRCodeGenerator()
        generator.add_data(name)
        generator.save_image(filename)

if __name__ == "__main__":
    main()
