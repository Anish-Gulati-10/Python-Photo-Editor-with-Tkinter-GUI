from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os

# Create the main window
root = Tk()
root.title("Simple Photo Editor")
root.geometry("640x700")  # Adjusted window size

# Global variables
current_img = None
img_width = 0
img_height = 0
img_path = None
direction = 1  # 1 for increasing, -1 for decreasing

# Function to open a file dialog and display the selected image
def selected():
    global current_img, img_width, img_height, img_path
    img_path = filedialog.askopenfilename(initialdir=os.getcwd())
    current_img = Image.open(img_path)
    current_img.thumbnail((580, 400))

    img1 = ImageTk.PhotoImage(current_img)
    canvas2.create_image(300, 210, image=img1)
    canvas2.image = img1

# Function to apply blur to the image
def blur(event):
    global current_img
    for m in range(0, v1.get()+1):
        current_img = current_img.filter(ImageFilter.BoxBlur(m))
    img1 = ImageTk.PhotoImage(current_img)
    canvas2.create_image(300, 210, image=img1)
    canvas2.image = img1

# Function to adjust brightness of the image
def brightness(event):
    global current_img, direction
    for m in range(0, v2.get()+1):
        imgg = ImageEnhance.Brightness(current_img)
        current_img = imgg.enhance(1 + direction * m / 10.0)
        img1 = ImageTk.PhotoImage(current_img)
        canvas2.create_image(300, 210, image=img1)
        canvas2.image = img1

# Function to adjust contrast of the image
def contrast(event):
    global current_img, direction
    for m in range(0, v3.get()+1):
        imgg = ImageEnhance.Contrast(current_img)
        current_img = imgg.enhance(1 + direction * m / 10.0)
        img1 = ImageTk.PhotoImage(current_img)
        canvas2.create_image(300, 210, image=img1)
        canvas2.image = img1

# Function to rotate the image
def rotate_image(event):
    global current_img
    current_img = current_img.rotate(int(rotate_combo.get()))
    img1 = ImageTk.PhotoImage(current_img)
    canvas2.create_image(300, 210, image=img1)
    canvas2.image = img1

# Function to flip the image
def flip_image(event):
    global current_img
    if flip_combo.get() == "FLIP LEFT TO RIGHT":
        current_img = current_img.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_combo.get() == "FLIP TOP TO BOTTOM":
        current_img = current_img.transpose(Image.FLIP_TOP_BOTTOM)
    img1 = ImageTk.PhotoImage(current_img)
    canvas2.create_image(300, 210, image=img1)
    canvas2.image = img1

# Function to add border to the image
def image_border(event):
    global current_img
    current_img = ImageOps.expand(current_img, border=int(border_combo.get()), fill=95)
    img1 = ImageTk.PhotoImage(current_img)
    canvas2.create_image(300, 210, image=img1)
    canvas2.image = img1

# Function to resize the image
def resize_image():
    global current_img, img_width, img_height
    new_width = simpledialog.askinteger("Resize", "Enter the new width:")
    new_height = simpledialog.askinteger("Resize", "Enter the new height:")
    if new_width is not None and new_height is not None:
        current_img = current_img.resize((new_width, new_height))
        img1 = ImageTk.PhotoImage(current_img)
        canvas2.create_image(300, 210, image=img1)
        canvas2.image = img1

# Function to compress and save the image
def compress_image():
    global current_img, img_path
    compression_quality = simpledialog.askinteger("Compress", "Enter the compression quality (1-95):", minvalue=1, maxvalue=95)
    if compression_quality is not None:
        ext = img_path.split(".")[-1]
        file = filedialog.asksaveasfilename(defaultextension=f".{ext}", filetypes=[("All Files", "*.*"), ("PNG file", "*.png"), ("JPEG file", "*.jpg")])
        if file:
            current_img.save(file, quality=compression_quality)

# Function to save the edited image
def save():
    global current_img, img_path
    ext = img_path.split(".")[-1]
    file = asksaveasfilename(defaultextension=f".{ext}", filetypes=[("All Files", "*.*"), ("PNG file", "*.png"), ("jpg file", "*.jpg")])
    if file:
        current_img.save(file)

# Create labels, scales, and comboboxes
blurr = Label(root, text="Blur:", font=("ariel 12 bold"), width=9, anchor='e')
blurr.place(x=15, y=8)

v1 = IntVar()
scale1 = ttk.Scale(root, from_=0, to=10, variable=v1, orient=HORIZONTAL, command=blur)
scale1.place(x=150, y=8)

bright = Label(root, text="Brightness:", font=("ariel 12 bold"))
bright.place(x=15, y=50)

v2 = IntVar()
scale2 = ttk.Scale(root, from_=0, to=10, variable=v2, orient=HORIZONTAL, command=brightness)
scale2.place(x=150, y=50)

contrastt = Label(root, text="Contrast:", font=("ariel 12 bold"))
contrastt.place(x=35, y=92)

v3 = IntVar()
scale3 = ttk.Scale(root, from_=0, to=10, variable=v3, orient=HORIZONTAL, command=contrast)
scale3.place(x=150, y=92)

rotate = Label(root, text="Rotate:", font=("ariel 12 bold"))
rotate.place(x=375, y=8)

values = [0, 90, 180, 270, 360]
rotate_combo = ttk.Combobox(root, values=values, font=('ariel 10 bold'))
rotate_combo.place(x=460, y=15)
rotate_combo.bind("<<ComboboxSelected>>", rotate_image)

flip = Label(root, text="Flip:", font=("ariel 12 bold"))
flip.place(x=400, y=50)

values1 = ["FLIP LEFT TO RIGHT", "FLIP TOP TO BOTTOM"]
flip_combo = ttk.Combobox(root, values=values1, font=('ariel 10 bold'))
flip_combo.place(x=460, y=57)
flip_combo.bind("<<ComboboxSelected>>", flip_image)

border = Label(root, text="Add border:", font=("ariel 12 bold"))
border.place(x=340, y=92)

values2 = [i for i in range(10, 45, 5)]
border_combo = ttk.Combobox(root, values=values2, font=("ariel 10 bold"))
border_combo.place(x=460, y=99)
border_combo.bind("<<ComboboxSelected>>", image_border)

# create canvas to display image
canvas2 = Canvas(root, width="600", height="420", relief=RIDGE, bd=2)
canvas2.place(x=15, y=150)

# create buttons
btn_resize = Button(root, text="Resize", bg='black', fg='gold', font=('ariel 12 bold'), relief=GROOVE, command=resize_image)
btn_resize.place(x=555, y=600)

btn_compress = Button(root, text="Compress and Save", bg='black', fg='gold', font=('ariel 12 bold'), relief=GROOVE, command=compress_image)
btn_compress.place(x=100, y=650)

btn_select = Button(root, text="Select Image", bg='black', fg='gold', font=('ariel 12 bold'), relief=GROOVE, command=selected)
btn_select.place(x=15, y=600)

btn_save = Button(root, text="Save", bg='black', fg='gold', font=('ariel 12 bold'), relief=GROOVE, command=save)
btn_save.place(x=15, y=650)

btn_exit = Button(root, text="Exit", bg='black', fg='gold', font=('ariel 12 bold'), relief=GROOVE, command=root.destroy)
btn_exit.place(x=575, y=650)

# Start the main loop
root.mainloop()
