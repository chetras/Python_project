import tkinter as tk
from tkinter import *
import mysql.connector
import os
from tkinter import messagebox


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
button_font = ("Arial", 15)  # Custom font for buttons
entry_font = ("Arial", 12)  # Custom font for entries

# Function to add product to the database and display in the table
def add_product():
    values = [entry.get() for entry in form_entries]
    cursor.execute("INSERT INTO Products (id, name, type, price, stock) VALUES (%s, %s, %s, %s, %s)", values)
    connection.commit()
    table.insert("", "end", values=values)

def update_product():
    print(1)



def del_product():
    selected_item = table.selection()
    if selected_item:
        # Delete from the database
        item_id = table.item(selected_item, "values")[0]
        cursor.execute("DELETE FROM Products WHERE id = %s", (item_id,))
        connection.commit()
        
        # Delete from the table view
        table.delete(selected_item)
    else:
        messagebox.showinfo("Please select a product you want to delete") 

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

def search_product():
    search_query = search_entry.get()
    cursor.execute("SELECT * FROM Products WHERE id = %s OR name LIKE %s", (search_query, '%' + search_query + '%'))
    # Clear the table before populating with search results
    for item in table.get_children():
        table.delete(item)
    for row in cursor.fetchall():
        table.insert("", "end", values=row)
# Button Click Functions
def products_click():
    print("Products button clicked")

def customers_click():
    print("Customers button clicked")

def manage_click():
    print("Manage button clicked")

def exit_click():
    window.destroy()
    os.system('python login.py')

img = PhotoImage(file='store.png')
img = img.subsample(4)
Label(window, image=img, bg='white').place(x=120, y=100)

# Frame for Buttons
button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x")

# Buttons for Products, Customers, Manage, Exit
products_button = tk.Button(button_frame, text="Products", font=button_font, command=products_click, width=10,padx=10)
products_button.pack(side="left",padx=20)

customers_button = tk.Button(button_frame, text="Customers", font=button_font, command=customers_click, width=10,padx=10)
customers_button.pack(side="left", padx=20)

manage_button = tk.Button(button_frame, text="Manage", font=button_font, command=manage_click, width=10)
manage_button.pack(side="left",padx= 20)

search_button = tk.Button(button_frame, text="Search", font=button_font, width=10, command=search_product)
search_button.pack(side="right", padx=10, pady=10, anchor=E)

search_entry = tk.Entry(button_frame, font=button_font)
search_entry.pack(side="right", padx=10, anchor=E)

signout_button = tk.Button(window, text="Sign Out", font=button_font, command=exit_click, width=10)
signout_button.pack(side="bottom", anchor="sw", padx=20, pady=10)

# signout_button = tk.Button(button_frame, text="Sign Out", font=button_font, command=exit_click, width=10)
# signout_button.pack(side="right", padx = 30)

# Icon Area
icon_label = tk.Frame(window, height=50, width=100)
icon_label.pack(side="left", padx=10)

# Form Fields
form_frame = tk.Frame(window)
form_frame.place(x=100, y=20)
form_frame.pack(side="left", padx=10)

form_labels = [ "Pro.#","Pro. Name", "Type", "Price", "Stock"]
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

add_button = tk.Button(buttons_frame, text="Add", width=10, command=add_product)
add_button.pack(fill="x", padx=5, pady=10)

update_button = tk.Button(buttons_frame, text="Update", width=10, command=update_product)
update_button.pack(fill="x", padx=5, pady=10)

del_button = tk.Button(buttons_frame, text="Delete", width=10, command=del_product)
del_button.pack(fill="x", padx=5, pady=10)

showall_button = tk.Button(buttons_frame, text="Show all", width=10, command=show_product)
showall_button.pack(fill="x", padx=5, pady=10)



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

window.mainloop()
