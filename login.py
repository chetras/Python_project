from tkinter import *
from tkinter import messagebox
import subprocess
import mysql.connector

root = Tk()
root.title('Login')
root.geometry('925x680+300+200')
root.configure(bg='#fff')
root.resizable(False, False)
user_id = None  # Store the logged-in user ID

def signin():
    username=user.get()
    password=code.get()
    try:
        # Establish Connection
        conn = mysql.connector.connect(
            user="root",
            password="bormeysql", # Change it to your password
            host="localhost",
            database="Shop"
        )

        cursor = conn.cursor()

        if username == 'admin' and password=='12345':
            messagebox.showinfo("Login Granted", "Welcome, Admin!")
            root.destroy()
            # subprocess.run(['python', 'admin_product.py'])  
            import admin_product
            admin_product.window()

        else:
            sql = "SELECT * FROM user_account WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))

            result = cursor.fetchone()

            if result: 
                user_id = result[0]

                with open('user_id.txt', 'w') as file:
                    file.write(str(user_id))

                update_logged_in_status(cursor, user_id, 1)
                conn.commit()
                messagebox.showinfo("Login Granted", "Welcome to Our Shop!")
                root.destroy()
                # subprocess.run(['python', 'user_shop.py'])
                import user_shop
                user_shop.window()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        conn.close()
    except mysql.connector.Error as err: 
        messagebox.showerror("Error", f"An error occurred: {str(err)}")

def update_logged_in_status(cursor, user_id, status):
    update_sql = "UPDATE user_account SET logged_in = %s WHERE id = %s"
    cursor.execute(update_sql, (status, user_id))

def sign_out():
    # Retrieving the user_id from the file
    with open('user_id.txt', 'r') as file:
        user_id = int(file.read())

    if user_id:
        try:
            conn = mysql.connector.connect(
                user="root",
                password="bormeysql", # Change the password
                host="localhost",
                database="Shop"
            )

            cursor = conn.cursor()
            update_logged_in_status(cursor, user_id, 0)  # Set logged_in status to 0 for the logged-out user
            conn.commit()
            user_id = None  # Reset the user ID

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {str(err)}")
    root.destroy()  # Close the application


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


def on_enter_password(e):
    if code.get() == 'Password':
        code.delete(0, 'end')
        code.config(show="*")

def on_leave_password(e):
    if code.get() == '':
        code.config(show="")
        code.insert(0, 'Password')

code = Entry(frame, fg='black', border=0, bg='white', highlightbackground='white', highlightthickness=0, font=('Lato', 16))
code.place(x=50, y=220)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter_password)
code.bind('<FocusOut>', on_leave_password)

def open_signup_screen():
    root.destroy()
    # subprocess.run(['python', 'signup.py'])   
    import signup
    signup.window()
    


Frame(frame, width=320, height=3, bg='#856947').place(x=50, y=250)

Button(frame, width=32, height=2, text='Sign in', highlightbackground='#856947', bg='#856947', fg='black', border=0, command=signin).place(x=50, y=300)

label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Lato', 14))
label.place(x=50, y=365)

sign_up = Button(frame, width=8, height=2, text='Sign up', border=0, highlightbackground='#856947', cursor='hand2', fg='black',command=open_signup_screen)
sign_up.place(x=270, y=360)

root.protocol("WM_DELETE_WINDOW", sign_out)  
root.mainloop()