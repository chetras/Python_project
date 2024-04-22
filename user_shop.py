import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import messagebox
import subprocess
from tkinter import ttk


with open('user_id.txt', 'r') as file:
        user_id = int(file.read())
# Create the main window
window = tk.Tk()
window.title("User Shop")
window.geometry('1000x680+300+200')
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

# Custom Font for Buttons
button_font = ("Lato", 15) 
entry_font = ("Lato", 12)  

def sign_out():
    with open('user_id.txt', 'r') as file:
        user_id = int(file.read())
    if user_id:
        try:
            conn = mysql.connector.connect(
                user="root",
                password="bormeysql", #Change the password
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

def update_stock(product_id, quantity):
    # Retrieve current stock from the database
    cursor.execute("SELECT stock FROM Products WHERE id = %s", (product_id,))
    current_stock = int(cursor.fetchone()[0])  # Convert to float

    # Calculate new stock
    new_stock = current_stock - quantity

    # Update stock in the database
    cursor.execute("UPDATE Products SET stock = %s WHERE id = %s", (new_stock, product_id))
    connection.commit()

    # Refresh the table view
    populate_table()
    
def show_receipt(product_id, product_name, quantity, total_amount, user_id, amount):
    # Retrieve the username from the database based on the user_id
    cursor.execute("SELECT username FROM user_account WHERE id = %s", (user_id,))
    username = cursor.fetchone()[0]  # Assuming there is only one row for the user_id

    # Calculate the change
    change = amount - total_amount

    # Create a new pop-up window for the receipt
    receipt_window = tk.Toplevel(window)
    receipt_window.resizable(False,False)
    receipt_window.title("Receipt Info")

    # Display the receipt information including username and change
    receipt_info = f"Username: {username}\nProduct ID: {product_id}\nProduct Name: {product_name}\nQuantity: {quantity}\nTotal Amount: ${total_amount}\nPayment Amount: ${amount}\nChange: ${change if change >= 0 else 0}"
    receipt_label = tk.Label(receipt_window, text=receipt_info, font=("Lato", 12))
    receipt_label.pack(padx=20, pady=10)

def pay_product():
    product_id = form_entries[0].get()
    product_name = form_entries[1].get()
    quantity = int(form_entries[2].get())
    amount = float(amount_entry.get())  # Get the amount entered by the user
    total_amount = float(total_label.cget("text").split("$")[1])  # Get the total amount from the label

    if amount >= total_amount:
        # Payment successful
        messagebox.showinfo("Payment Successful", "Payment has been successfully processed.")

        # Insert order information into the user_order table
        cursor.execute("INSERT INTO user_order (id, user_id, name, quantity, total, Amount) VALUES (%s, %s, %s, %s, %s, %s)",
                       (product_id, user_id, product_name, quantity, total_amount, amount))
        connection.commit()

        # Show receipt information in a pop-up window
        show_receipt(product_id, product_name, quantity, total_amount, user_id, amount)

        # Update stock in the Products table
        update_stock(product_id, quantity)

        # Clear the entries and reset the total amount
        clear_entries()
        total_label.config(text="Total:")
        # Clear the amount entry field
        amount_entry.delete(0, 'end')

    else:
        # Insufficient payment
        messagebox.showerror("Insufficient Payment", "The amount entered is insufficient for the total.")

def calculate_total():
    # Retrieve the values entered by the user
    product_id = form_entries[0].get()
    product_name = form_entries[1].get()
    quantity = int(form_entries[2].get())

    # Check if the product exists in the database
    cursor.execute("SELECT * FROM Products WHERE id = %s AND name = %s", (product_id, product_name))
    product = cursor.fetchone()

    if product:
        _, _, _, price, stock = product
        price = float(price)  # Convert price to a numeric type
        stock = float(stock)  # Convert stock to an integer

        if quantity > stock:
            messagebox.showerror("Insufficient Stock", "The quantity entered is greater than the available stock.")
        else:
            # Calculate the total amount
            total_amount = price * quantity

            # Display the total amount
            total_label.config(text="Total: $" + str(total_amount))
    else:
        # Show an error message if the product does not exist
        messagebox.showerror("Product Not Found", "The product with the specified ID and name does not exist.")


def retrieve_price_from_database(product_id):
    # Query the database to retrieve the price of the product
    cursor.execute("SELECT price FROM Products WHERE id = %s", (product_id,))
    price = cursor.fetchone()
    if price:
        return price[0]
    else:
        return None
    
    
def cancel_product():
    # Clear the entries
    clear_entries()
    # Reset the total amount to blank
    total_label.config(text="Total:")

def show_product():
     # Clear the table before repopulating with all data
    for item in table.get_children():
        table.delete(item)
    # Repopulate the table with all data
    populate_table()

# Function to populate the table view with data from the database
def populate_table():
    # Clear the table before repopulating with all data
    for item in table.get_children():
        table.delete(item)

    # Repopulate the table with all data
    cursor.execute("SELECT * FROM Products")
    for row in cursor.fetchall():
        table.insert("", "end", values=row)


def acc_click():
    window.destroy()
    # subprocess.run(['python', 'user_account.py']) 
    import user_account
    user_account.window()


def exit_click():
    window.destroy()
    # subprocess.run(['python', 'login.py'])
    import login
    login.window()


# Frame for Buttons
button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x")

# Buttons for Products, Customers, Manage, Exit
shop_button = tk.Button(button_frame, text="Shop", font=button_font, width=10,padx=10)
shop_button.pack(side="left",padx=20)

account_button = tk.Button(button_frame, text="Account", font=button_font, command=acc_click, width=10,padx=10)
account_button.pack(side="left", padx=20)

signout_button = tk.Button(window, text="Sign Out", font=button_font, command=exit_click, width=10)
signout_button.pack(side="bottom", anchor="sw", padx=20, pady=10)


# Form Fields
form_frame = tk.Frame(window)
form_frame.place(x=100, y=20)
form_frame.pack(side="left", padx=40)

# Add a label above the entry fields
order_label = tk.Label(form_frame, text="Order Here", font=("Lato", 30))
order_label.pack(anchor="w", pady=(0, 10))  # Add some vertical padding


form_labels = [ "Product #ID","Product Name", "Quantity"]
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
pay_button.pack(fill="x",  pady=10)

total_button = tk.Button(buttons_frame, text="Calculate Total", width=10, command=calculate_total)
total_button.pack(fill="x",  pady=10)

cancel_button = tk.Button(buttons_frame, text="Cancel", width=10, command=cancel_product)
cancel_button.pack(fill="x",  pady=10)

# Table
table_frame = tk.Frame(window)
table_frame.pack(side="left", pady=10, fill="both", expand=True)

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