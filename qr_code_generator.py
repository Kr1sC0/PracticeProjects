import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import re
import qrcode
from pyzbar.pyzbar import decode


def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Easy QR Generator")
        self.geometry("800x600")  # Set the size of the window

        self.create_menu()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        main_frame = tk.Frame(self, width=750, height=550, bg="#3D6466")
        main_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        frame = InputForm(main_frame)
        frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    def create_menu(self):
        menu_bar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file_dialog)
        file_menu.add_command(label="Save", command=self.save_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.decode_qr_code(file_path)

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg;*.jpeg")])
        if file_path:
            self.save_qr_code(file_path)
    def show_usage(self):
        ...
        
    def show_about(self):
        messagebox.showinfo("About", "Easy QR Generator v1.0\nDeveloped by Kristian Hughes")

    def decode_qr_code(self, file_path=None):
        if file_path:
            result = decode_img(file_path)
            print(f"Decoded data: {result}")


class InputForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=0, column=0, columnspan=1, sticky='ew')

        # Bind enter button to add_to_list
        self.entry.bind("<Return>", self.add_to_list)

        self.entry_btn2 = ttk.Button(self, text="Delete", command=self.delete_from_list)
        self.entry_btn2.grid(row=0, column=2)

        self.entry_btn = ttk.Button(self, text="Add", command=self.add_to_list)
        self.entry_btn.grid(row=0, column=1)

        self.text_list = tk.Listbox(self)
        self.text_list.grid(row=1, column=0, columnspan=3, sticky='nsew')

        # Add buttons for QR code functions
        self.generate_qr_btn = ttk.Button(self, text="Generate QR Code", command=self.generate_qr_code)
        self.generate_qr_btn.grid(row=2, column=0, sticky='ew')

        self.decode_qr_btn = ttk.Button(self, text="Decode QR Code", command=self.open_file_dialog)
        self.decode_qr_btn.grid(row=2, column=1, sticky='ew')

        self.display_qr_btn = ttk.Button(self, text="Display QR Code", command=self.display_qr_code)
        self.display_qr_btn.grid(row=2, column=2, sticky='ew')

        # Label to display the QR code image
        self.qr_image_label = ttk.Label(self)
        self.qr_image_label.grid(row=3, column=0, columnspan=3, sticky='nsew')

    def add_to_list(self, event=None):
        if text := self.entry.get():
            self.text_list.insert(tk.END, text)
            self.entry.delete(0, tk.END)

    def delete_from_list(self, event=None):
        selected_items = self.text_list.curselection()
        for index in reversed(selected_items):
            self.text_list.delete(index)

    def generate_qr_code(self):
        text = self.entry.get()
        if text:
            filename = "qr_code.png"
            img = text_to_qr(valid_url(text), filename)
            self.entry.delete(0, tk.END)
            print(f"QR Code saved as {filename}")
            self.display_image(img)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.decode_qr_code(file_path)

    def display_qr_code(self):
        text = self.entry.get()
        if text:
            img = QRCodeGenerator().generate_image(valid_url(text))
            self.display_image(img)

    def display_image(self, img):
        img = img.convert("RGB")
        img_tk = ImageTk.PhotoImage(img)
        self.qr_image_label.config(image=img_tk)
        self.qr_image_label.image = img_tk
        

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

def valid_url(link: str):
    pattern = re.compile(r'^(https?:\/\/)?([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(:[0-9]{1,5})?(\/.*)?$')
    if pattern.match(link):
        return link
    else:
        print("Invalid link. Please try again.")
        return None

def display_qr_code(qr_image):
    ...

def text_to_qr(text: str, filename: str):
    generator = QRCodeGenerator()
    generator.add_data(text)
    if filename:
        generator.save_image(filename)
    return generator.generate_image()

def decode_img(image_path: str) -> str:
    """
    Decode QR code image
    :usage: str
    :param: image_name.png
    """
    img = Image.open(image_path)
    decode_objects = decode(img)
    for obj in decode_objects:
        return obj.data.decode('utf-8')
    img.close()

if __name__ == "__main__":
    main()
