import tkinter as tk
from tkinter import *
import mysql.connector
import os
from tkinter import messagebox
import subprocess


from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title("Product Management System")
window.geometry('1000x680+300+200')
window.resizable(False, False)

# Establish Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chetra1234",  # Change it to your password
    database="Shop"
)

# Create a cursor
cursor = connection.cursor()

# Custom Font for Buttons
button_font = ("Lato", 15)  # Custom font for buttons
entry_font = ("Lato", 12)  # Custom font for entries

def clear_entries():
    for entry in form_entries:
        entry.delete(0, 'end')


def show_product():
     # Clear the table before repopulating with all data
    for item in table.get_children():
        table.delete(item)
    # Repopulate the table with all data
    populate_table()

# Function to populate the table view with data from the database
def populate_table():
    cursor.execute("SELECT * FROM user_account")
    for row in cursor.fetchall():
        table.insert("", "end", values=row)

def search_product():
    # Get the user ID from the entry field
    username_id = form_entries[0].get()  # Assuming the user ID entry is at index 0

    # Clear the table before performing the search
    for item in table.get_children():
        table.delete(item)

    # Query the database for the user ID
    cursor.execute("SELECT * FROM user_account WHERE id = %s", (username_id,))
    
    # Populate the table with the search result
    for row in cursor.fetchall():
        table.insert("", "end", values=row)

    clear_entries()
    
# Button Click Functions
def products_click():
    window.destroy()
    subprocess.run(['python', 'admin_product.py'])


def manage_click():
    window.destroy()
    subprocess.run(['python', 'admin_manage.py'])

def exit_click():
    window.destroy()
    subprocess.run(['python', 'login.py'])
img = PhotoImage(file='customer.png')
img = img.subsample(4)
Label(window, image=img, bg='white').place(x=120, y=100)

# Frame for Buttons
button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x")

# Buttons for Products, Customers, Manage, Exit
products_button = tk.Button(button_frame, text="Products", font=button_font, command=products_click, width=10,padx=10)
products_button.pack(side="left",padx=20)

customers_button = tk.Button(button_frame, text="Customers", font=button_font, width=10,padx=10)
customers_button.pack(side="left", padx=20)

manage_button = tk.Button(button_frame, text="Manage", font=button_font, command=manage_click, width=10)
manage_button.pack(side="left",padx= 20)

signout_button = tk.Button(window, text="Sign Out", font=button_font, command=exit_click, width=10)
signout_button.pack(side="bottom", anchor="sw", padx=20, pady=10)


# Icon Area
icon_label = tk.Frame(window, height=50, width=100)
icon_label.pack(side="left", padx=10)

# Form Fields
form_frame = tk.Frame(window)
form_frame.place(x=100, y=20)
form_frame.pack(side="left", padx=10)

form_labels = [ "User.#","User. Name"]
form_entries = []

for label_text in form_labels:
    label = tk.Label(form_frame, text=label_text, font=button_font)  # Increase font size for labels
    label.pack(anchor="w")
    entry = tk.Entry(form_frame, font=entry_font)  # Increase font size for entries
    entry.pack(anchor="w")
    form_entries.append(entry)


# Buttons
buttons_frame = tk.Frame(window)
buttons_frame.pack(side="left", padx=10)

search_button = tk.Button(buttons_frame, text="Search", width=10, command=search_product)
search_button.pack(fill="x", padx=5, pady=10)

showall_button = tk.Button(buttons_frame, text="Show all", width=10, command=show_product)
showall_button.pack(fill="x", padx=5, pady=10)

# Table
table_frame = tk.Frame(window)
table_frame.pack(side="left", padx=10, fill="both", expand=True)

columns = ("#", "Usrname", "password","Order", "Amount")
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

window.mainloop()