import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import messagebox
import subprocess
from tkinter import ttk


# Create the main window
window = tk.Tk()
window.title("User Account")
window.geometry('1000x680+300+200')
window.resizable(False, False)

# Establish Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bormeysql",  # Change the password
    database="Shop"
)

# Create a cursor
cursor = connection.cursor()

# Custom Font for Buttons
button_font = ("Lato", 15)  
entry_font = ("Lato", 12)  

# Retrieving the user_id from the file
with open('user_id.txt', 'r') as file:
    user_id = int(file.read())


# Function to populate the table view with data from the database
def populate_table():
    # Clear the table before repopulating with user-specific data
    for item in table.get_children():
        table.delete(item)

    # Retrieve user-specific data from the UserHistory table based on the user_id
    cursor.execute("SELECT id, name, quantity, total, Amount FROM user_order WHERE user_id = %s", (user_id,))
    for row in cursor.fetchall():
        table.insert("", "end", values=row)


def get_logged_in_username():
    # Retrieve the username from the user_account table based on the logged-in user
    cursor.execute("SELECT username FROM user_account WHERE logged_in = 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return ""
    

def sign_out():
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
    window.destroy()  # Close the application

def update_logged_in_status(cursor, user_id, status):
    update_sql = "UPDATE user_account SET logged_in = %s WHERE id = %s"
    cursor.execute(update_sql, (status, user_id))


# Button Click Functions
def shop_click():
    window.destroy()
    # subprocess.run(['python', 'user_shop.py'])
    import user_shop
    user_shop.window() 


def exit_click():
    window.destroy()
    # subprocess.run(['python', 'login.py'])
    import login
    login.window()


# Frame for Buttons
button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x")

# Buttons for Products, Customers, Manage, Exit
shop_button = tk.Button(button_frame, text="Shop", font=button_font, width=10,padx=10, command=shop_click)
shop_button.pack(side="left",padx=20)

account_button = tk.Button(button_frame, text="Account", font=button_font, width=10,padx=10)
account_button.pack(side="left", padx=20)

signout_button = tk.Button(window, text="Sign Out", font=button_font, command=exit_click, width=10)
signout_button.pack(side="bottom", anchor="sw", padx=20, pady=10)


# Buttons
buttons_frame = tk.Frame(window)
buttons_frame.pack(side="left", padx=10)

# Table
table_frame = tk.Frame(window)
table_frame.pack(side="left", padx=10, fill="both", expand=True, pady=10)

columns = ("ID", "Name", "Quantity","Total", "Payment Amount")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=100)
table.pack(side="left", fill="both", expand=True)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=scrollbar.set)

# Populate the table with data from the database
populate_table()
window.protocol("WM_DELETE_WINDOW", sign_out)  # Bind exit_click to window close

window.mainloop()