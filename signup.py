from tkinter import *
from tkinter import messagebox
import ast


window = Tk()
window.title('Sign Up')
window.geometry('925x680+300+200')
window.configure(bg='white')
window.resizable(False, False)


def signup():
    username=user.get()
    password=code.get()
    confirm_code= confirm_code.get()

    if password == confirm_code:
        try:
            file=open('datasheet.txt', 'r+')
            d=file.read()
            r = ast.literal_eval(d)

            dict2={username:password}
            r.update(dict2)
            file.truncate(0)
            file.close()

            file=open('datasheet.txt', 'w')
            w=file.write(str(r))

            messagebox.showeinfo('Signup', 'Successfully signed up!')

        except:
            file=open('datasheet.txt', 'w')
            pp=str({'Username': 'Password'})
            file.write(pp)
            file.close()
    
    else:
        messagebox.showerror('Invalid', 'Both passwords should match.')


# img = PhotoImage(file='Crystal Jewels.png')
# img = img.subsample(2)
# Label(window, image=img, bg='white').place(x=0, y=0)

frame = Frame(window, width=400, height=500, bg='white')
frame.place(x=480, y=50)


heading = Label(frame, text='Sign up', fg='#856947', bg='white', font=('Lato', 60, 'bold'))
heading.place(x=110, y=10)


# Username
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


# Password
def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')

code = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 16))
code.place(x=50, y=220)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=320, height=3, bg='#856947').place(x=50, y=250)


# Confirm Password
def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Confirm Password')

confirm_code = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 16))
confirm_code.place(x=50, y=290)
confirm_code.insert(0, 'Confirm Password')
confirm_code.bind('<FocusIn>', on_enter)
confirm_code.bind('<FocusOut>', on_leave)

Frame(frame, width=320, height=3, bg='#856947').place(x=50, y=320)


Button(frame, width=32, height=2, text='Sign up', highlightbackground='#856947', bg='#856947', fg='black', border=0, command=signup).place(x=50, y=350)

label = Label(frame, text="Already have an account?", fg='black', bg='white', font=('Lato', 14))
label.place(x=50, y=420)

sign_in = Button(frame, width=8, height=2, text='Sign in', border=0, highlightbackground='#856947', cursor='hand2', fg='black')
sign_in.place(x=265, y=415)

window.mainloop()