from tkinter import *
from tkinter import messagebox
import os
import subprocess

root = Tk()
root.title('Login')
root.geometry('925x680+300+200')
root.configure(bg='#fff')
root.resizable(False, False)

def signin():
    username=user.get()
    password=code.get()

    if username == 'admin' and password=='1234':
        screen=Toplevel(root)
        screen.title('App')
        screen.geometry('925x500+300+200')
        screen.config(bg='white')

        Label(screen, text='Hi brader!', bg='#fff', font=('Arial', 30, 'bold')).pack(expand=True)
        screen.mainloop()

    elif username != 'admin' and password!='1234':
        messagebox.showerror('Invalid', 'Invalid username and password.')

    elif username != 'admin':
        messagebox.showerror('Invalid', 'Invalid username.')

    elif password!='1234':
        messagebox.showerror('Invalid', 'Invalid password.')
    

img = PhotoImage(file='Crystal Jewels.png')
img = img.subsample(2)
Label(root, image=img, bg='white').place(x=0, y=0)

frame = Frame(root, width=400, height=500, bg='white')
frame.place(x=480, y=50)

heading = Label(frame, text='Sign in', fg='#856947', bg='white', font=('Lato', 60, 'bold'))
heading.place(x=110,y=10)


def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')

user = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 16))
user.place(x=50, y=150)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=320, height=3, bg='#856947').place(x=50, y=180)


def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')

def open_signup_screen():
    root.destroy()
    import signup 
    signup.window   

code = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 16))
code.place(x=50, y=220)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=320, height=3, bg='#856947').place(x=50, y=250)


Button(frame, width=32, height=2, text='Sign in', highlightbackground='#856947', bg='#856947', fg='black', border=0, command=signin).place(x=50, y=300)

label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Lato', 14))
label.place(x=50, y=365)

sign_up = Button(frame, width=8, height=2, text='Sign up', border=0, highlightbackground='#856947', cursor='hand2', fg='black',command=open_signup_screen)
sign_up.place(x=270, y=360)


root.mainloop()