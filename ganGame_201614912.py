import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import tkinter as tk
import random
from tensorflow.keras.datasets import fashion_mnist
from PIL import Image, ImageTk

(x_train, y_train),(x_test, y_test) = fashion_mnist.load_data() # data load
x_test = x_test[np.isin(y_test, [7])] # sneakersa data
generator = tf.keras.models.load_model("./fashion_gan.h5") # model load

img_size = 200
tk_img = ''
ftk_img = ''
count = 0
deceive = 0
rand = random.randrange(2)

def fake_sneakers() :
    global ftk_img
    img = generator.predict(np.random.normal(0, 1, (1, 100)))
    img = img.reshape(28, 28)
    img = ((img+1)/2)*255
    img = img.astype('int32')
    img = Image.fromarray(img)
    ftk_img = img.resize((img_size, img_size))
    ftk_img = ImageTk.PhotoImage(ftk_img)
    return ftk_img

def real_sneakers() :
    global tk_img
    img = random.choice(x_test)
    img = Image.fromarray(img)
    tk_img = img.resize((img_size, img_size))
    tk_img = ImageTk.PhotoImage(tk_img)
    return tk_img

def quit_program() :
    win.destroy()
    
def next() :
    global count, rand
    rand = random.randrange(2)
    fake_img = fake_sneakers()
    real_img = real_sneakers()
    imgs = [fake_img, real_img]
    canvas_0.create_image(img_size/2, img_size/2, image=imgs[1 if rand else 0])
    canvas_1.create_image(img_size/2, img_size/2, image=imgs[0 if rand else 1])
    count += 1
    label_count.configure(text=f'<속은 비율: {deceive}/{count}>, {deceive/count*100}')
    select0_button.config(text='<내가 진짜>')
    select1_button.config(text='<내가 진짜>')
    select0_button.config(state=tk.NORMAL)
    select1_button.config(state=tk.NORMAL)
    next_button.config(state=tk.DISABLED)

def select0() :
    global deceive
    select()
    if rand == 0 :
        deceive += 1

def select1() :
    global deceive
    select()
    if rand == 1 :
        deceive += 1
    
def select() :
    if rand == 0 :
        select0_button.config(text='FAKE')
        select1_button.config(text='REAL')
    else :
        select0_button.config(text='REAL')    
        select1_button.config(text='FAKE')
    select0_button.config(state=tk.DISABLED)
    select1_button.config(state=tk.DISABLED)
    next_button.config(state=tk.NORMAL)
    

win = tk.Tk()
win.title("Which fashion is real?")
win.geometry('700x300')

canvas_0 = tk.Canvas(win, width=230, height=230)
canvas_1 = tk.Canvas(win, width=230, height=230)
next_button = tk.Button(win, text="<다음으로>", command=next, state=tk.DISABLED)
quit_button = tk.Button(win, text="<끝내기>", command=quit_program)
select0_button = tk.Button(win, text="<내가 진짜>", command=select0)
select1_button = tk.Button(win, text="<내가 진짜>", command=select1)
label_count = tk.Label(win, width=13, height=1, text='start')

fake_img = fake_sneakers()
real_img = real_sneakers()
canvas_0.create_image(img_size/2, img_size/2, image=fake_img)
canvas_1.create_image(img_size/2, img_size/2, image=real_img)

canvas_0.grid(row=0, column=0)
canvas_1.grid(row=0, column=1)
select0_button.grid(row=1, column=0)
select1_button.grid(row=1, column=1)
next_button.grid(row=0, column=2)
quit_button.grid(row=0, column=3)
label_count.grid(row=1, column=3)

win.mainloop()