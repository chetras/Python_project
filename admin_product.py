import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import messagebox
import subprocess
from PIL import ImageTk, Image



from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title("Admin Products Page")
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

def clear_entries():
    for entry in form_entries:
        entry.delete(0, 'end')

# Function to add product to the database and display in the table
def add_product():
    values = [entry.get() for entry in form_entries]
    cursor.execute("INSERT INTO Products (id, name, type, price, stock) VALUES (%s, %s, %s, %s, %s)", values)
    connection.commit()
    table.insert("", "end", values=values)
    clear_entries()


def update_product():
    # Get the values from the entry fields
    id_value = form_entries[0].get()  # Assuming the ID entry is the first one in the form_entries list
    name_value = form_entries[1].get()
    type_value = form_entries[2].get()
    price_value = form_entries[3].get()
    stock_value = form_entries[4].get()

    # Update the values in the table view
    selected_item = table.selection()
    if selected_item:
        current_values = table.item(selected_item, "values")
        updated_values = [
            id_value if id_value else current_values[0],
            name_value if name_value else current_values[1],
            type_value if type_value else current_values[2],
            price_value if price_value else current_values[3],
            stock_value if stock_value else current_values[4]
        ]
        table.item(selected_item, values=updated_values)

        # Prepare the update query
        update_query = "UPDATE Products SET "
        data = []
        if id_value:
            update_query += "id = %s, "
            data.append(id_value)
        if name_value:
            update_query += "name = %s, "
            data.append(name_value)
        if type_value:
            update_query += "type = %s, "
            data.append(type_value)
        if price_value:
            update_query += "price = %s, "
            data.append(price_value)
        if stock_value:
            update_query += "stock = %s, "
            data.append(stock_value)

        # Remove the last comma and add the WHERE clause
        update_query = update_query[:-2] + " WHERE id = %s"
        data.append(current_values[0])

        # Update the values in the database
        cursor.execute(update_query, data)
        connection.commit()
        clear_entries()
    else:
        messagebox.showinfo("Wrong","Please select a product to update")


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
    window.destroy()
    # subprocess.run(['python', 'admin_customer.py'])
    import admin_customer
    admin_customer.window()

def manage_click():
    # print("Manage button clicked")
    window.destroy()
    import admin_manage
    admin_manage.window()

def exit_click():
    window.destroy()
    # subprocess.run(['python', 'login.py'])
    import login
    login.window()



# Frame for Buttons
button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x")

# Buttons for Products, Customers, Manage, Exit
products_button = tk.Button(button_frame, text="Products", font=button_font, command=products_click, width=10,padx=10)
products_button.pack(side="left",padx=20)

customers_button = tk.Button(button_frame, text="Customers", font=button_font, command=customers_click, width=10,padx=10)
customers_button.pack(side="left", padx=20)

manage_button = tk.Button(button_frame, text="Manage", font=button_font, command=manage_click, width=10, padx=10)
manage_button.pack(side="left",padx= 20)



search_entry = tk.Entry(button_frame, font=button_font)
search_entry.pack(side="right", padx=10, anchor=E)

signout_button = tk.Button(window, text="Sign Out", font=button_font, command=exit_click, width=10)
signout_button.pack(side="bottom", anchor="sw", padx=20, pady=10)


img = PhotoImage(file='store.png')
img = img.subsample(4)
Label(window, image=img, bg='white').place(x=25,y=70)



# Form Fields
form_frame = tk.Frame(window)
form_frame.pack(side="left", padx=25,anchor="w")

form_labels = [ "Product #ID","Product Name", "Type", "Price", "Stock"]
form_entries = []

for label_text in form_labels:
    label = tk.Label(form_frame, text=label_text, font=button_font)  
    label.pack(anchor="w")
    entry = tk.Entry(form_frame, font=entry_font)
    entry.pack(anchor="w")
    form_entries.append(entry)
    
search_button = tk.Button(button_frame, text="Search", font=button_font, command=search_product)
search_button.pack(side="right", padx=10, pady=10, anchor=E)



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
table_frame.pack(side="top", padx=10, fill="both", expand=True, pady=10)

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