from tkinter import *
from tkinter import messagebox
import mysql.connector
import subprocess

window = Tk()
window.title('Sign Up')
window.geometry('925x680+300+200')
window.configure(bg='white')
window.resizable(False, False)

# Establish Connection 
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bormeysql",  # Change it to your password
    database="Shop"
)

# Create a cursor
cursor = connection.cursor()

def signup():
    username = user.get()
    password = code.get()
    confirm_password = confirm_code.get()

    try:
        # Check if the username already exists in the database
        cursor.execute("SELECT * FROM user_account WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror('Error', 'Username already exists. Please choose a different username.')
        else:
            if password == confirm_password:
                # Insert user data into the database
                query = "INSERT INTO user_account (username, password) VALUES (%s, %s)"
                data = (username, password)
                cursor.execute(query, data)
                connection.commit()

                messagebox.showinfo('Signup', 'Successfully signed up!')

                # Clear the entry fields
                user.delete(0, 'end')
                code.delete(0, 'end')
                confirm_code.delete(0, 'end')
            else:
                messagebox.showerror('Invalid', 'Both passwords should match.')
    except mysql.connector.Error as error:
        messagebox.showerror('Error', f'Failed to insert record into user_account table: {error}')



img = PhotoImage(file='Crystal Jewels.png')
img = img.subsample(2)
Label(window, image=img, bg='white').place(x=0, y=0)

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

def open_login_screen():
    window.destroy()
    # subprocess.run(['python', 'login.py'])  
    import login
    login.window()


user = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 16))
user.place(x=50, y=150)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=320, height=3, bg='#856947').place(x=50, y=180)


# Password
def on_enter_password(e):
    if code.get() == 'Password':
        code.delete(0, 'end')
        code.config(show="*")  # Show asterisks for password entry

def on_leave_password(e):
    if code.get() == '':
        code.insert(0, 'Password')
        code.config(show="")  # Show default text for password entry

code = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 16))
code.place(x=50, y=220)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter_password)
code.bind('<FocusOut>', on_leave_password)

Frame(frame, width=320, height=3, bg='#856947').place(x=50, y=250)


# Confirm Password
def on_enter_confirm_password(e):
    if confirm_code.get() == 'Confirm Password':
        confirm_code.delete(0, 'end')
        confirm_code.config(show="*")  # Show asterisks for confirm password entry

def on_leave_confirm_password(e):
    if confirm_code.get() == '':
        confirm_code.insert(0, 'Confirm Password')
        confirm_code.config(show="")  # Show default text for confirm password entry

confirm_code = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 16))
confirm_code.place(x=50, y=290)
confirm_code.insert(0, 'Confirm Password')
confirm_code.bind('<FocusIn>', on_enter_confirm_password)
confirm_code.bind('<FocusOut>', on_leave_confirm_password)

Frame(frame, width=320, height=3, bg='#856947').place(x=50, y=320)


Button(frame, width=32, height=2, text='Sign up', highlightbackground='#856947', bg='#856947', fg='black', border=0, command=signup).place(x=50, y=350)

label = Label(frame, text="Already have an account?", fg='black', bg='white', font=('Lato', 14))
label.place(x=50, y=420)

sign_in = Button(frame, width=8, height=2, text='Sign in', border=0, highlightbackground='#856947', cursor='hand2', fg='black',command=open_login_screen)
sign_in.place(x=265, y=415)

window.mainloop()