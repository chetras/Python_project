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

def sign_out():
    # Retrieving the user_id from the file
    with open('user_id.txt', 'r') as file:
        user_id = int(file.read())

    if user_id:
        try:
            conn = mysql.connector.connect(
                user="root",
                password="Chetra1234",
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


def clear_entries():
    for entry in form_entries:
        entry.delete(0, 'end')

def  pay_product():
    print(1)

def receipt_product():
    print(1)
def show_product():
     # Clear the table before repopulating with all data
    for item in table.get_children():
        table.delete(item)
    # Repopulate the table with all data
    populate_table()

# Function to populate the table view with data from the database
def populate_table():
    cursor.execute("SELECT * FROM Products")
    for row in cursor.fetchall():
        table.insert("", "end", values=row)

# def search_product():
#     search_query = search_entry.get()
#     cursor.execute("SELECT * FROM Products WHERE id = %s OR name LIKE %s", (search_query, '%' + search_query + '%'))
#     # Clear the table before populating with search results
#     for item in table.get_children():
#         table.delete(item)
#     for row in cursor.fetchall():
#         table.insert("", "end", values=row)
# Button Click Functions
def products_click():
    print("Products button clicked")

def customers_click():
    print("Customers button clicked")

def manage_click():
    print("Manage button clicked")

def exit_click():
    window.destroy()
    subprocess.run(['python', 'login.py'])


# Frame for Buttons
button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x")

# Buttons for Products, Customers, Manage, Exit
shop_button = tk.Button(button_frame, text="Shop", font=button_font, command=products_click, width=10,padx=10)
shop_button.pack(side="left",padx=20)

account_button = tk.Button(button_frame, text="Account", font=button_font, command=customers_click, width=10,padx=10)
account_button.pack(side="left", padx=20)

signout_button = tk.Button(window, text="Sign Out", font=button_font, command=exit_click, width=10)
signout_button.pack(side="bottom", anchor="sw", padx=20, pady=10)

# Icon Area
icon_label = tk.Frame(window, height=50, width=100)
icon_label.pack(side="left", padx=10)

# Form Fields
form_frame = tk.Frame(window)
form_frame.place(x=100, y=20)
form_frame.pack(side="left", padx=10,pady=20)

# Add a label above the entry fields
order_label = tk.Label(form_frame, text="Order Here", font=("Lato", 30))
order_label.pack(anchor="w", pady=(0, 10))  # Add some vertical padding


form_labels = [ "Pro.#","Pro. Name", "Quantity"]
form_entries = []

for label_text in form_labels:
    label = tk.Label(form_frame, text=label_text, font=button_font)  # Increase font size for labels
    label.pack(anchor="w")
    entry = tk.Entry(form_frame, font=entry_font)  # Increase font size for entries
    entry.pack(anchor="w")
    form_entries.append(entry)

# Add a label under the entry fields to display the total amount
total_label = tk.Label(form_frame, text="Total:", font=("Lato", 15))
total_label.pack(anchor="w", pady=(10, 0))  # Add some vertical padding

amount_label = tk.Label(form_frame, text="Amount:", font=("Lato", 15))
amount_label.pack(anchor="w", pady=(10, 0))  # Add some vertical padding

amount_entry = tk.Entry(form_frame, font=entry_font)  # Increase font size for entries
amount_entry.pack(anchor="w")
# Buttons
buttons_frame = tk.Frame(window)
buttons_frame.pack(side="left", padx=10)

pay_button = tk.Button(buttons_frame, text="Pay", width=10, command=pay_product)
pay_button.pack(fill="x", padx=5, pady=10)

receipt_button = tk.Button(buttons_frame, text="Receipt", width=10, command=receipt_product)
receipt_button.pack(fill="x", padx=5, pady=10)


# Table
table_frame = tk.Frame(window)
table_frame.pack(side="left", padx=10, fill="both", expand=True)

columns = ("#", "Name", "Type", "Price", "Stock")
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
