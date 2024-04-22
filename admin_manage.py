import tkinter as tk
from tkinter import *
import mysql.connector
from tkinter import messagebox
import subprocess
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main window
window = tk.Tk()
window.title("Admin Manage Page")
window.geometry('1000x680+300+200')

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

def products_click():
    window.destroy()
    # subprocess.run(['python', 'admin_product.py'])
    import admin_product
    admin_product.window()

def customers_click():
    window.destroy()
    # subprocess.run(['python', 'admin_customer.py'])
    import admin_customer
    admin_customer.window()

def exit_click():
    window.destroy()
    # subprocess.run(['python', 'login.py'])
    import login
    login.window()

# Frame for Buttons
button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x")

# Buttons for Products, Customers, Manage, Exit
products_button = tk.Button(button_frame, text="Products", font=button_font, command=products_click, width=10, padx=10)
products_button.pack(side="left", padx=20)

customers_button = tk.Button(button_frame, text="Customers", font=button_font, command=customers_click, width=10, padx=10)
customers_button.pack(side="left", padx=20)

manage_button = tk.Button(button_frame, text="Manage", font=button_font, width=10)
manage_button.pack(side="left", padx=20)

signout_button = tk.Button(button_frame, text="Sign Out", font=button_font, command=exit_click, width=10)
signout_button.pack(side="right", padx=20)

# Retrieve data for total income from user_order table
cursor.execute("SELECT total FROM user_order")
total_income_data = [row[0] for row in cursor.fetchall()]

# Retrieve order numbers
order_numbers = list(range(1, len(total_income_data) + 1))

# Retrieve data for stock of each product from Products table
cursor.execute("SELECT name, stock FROM Products")
products_data = cursor.fetchall()
product_names = [row[0] for row in products_data]
product_stock = [float(row[1]) for row in products_data]  # Convert stock from string to int

# Sort the product stock and product names in ascending order
sorted_product_stock, sorted_product_names = zip(*sorted(zip(product_stock, product_names)))


# Create line graph for total income
fig_total_income = Figure(figsize=(6, 4))
ax_total_income = fig_total_income.add_subplot(111)
ax_total_income.plot(order_numbers, total_income_data)
ax_total_income.set_title('Total Income Over Time')
ax_total_income.set_xlabel('Order Number')
ax_total_income.set_ylabel('Total Income')

# Set x-axis ticks to integer values starting from 1
ax_total_income.set_xticks(order_numbers)

canvas_total_income = FigureCanvasTkAgg(fig_total_income, master=window)
canvas_total_income.draw()
canvas_total_income.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create bar chart for product stock
fig_product_stock = Figure(figsize=(8, 6))
ax_product_stock = fig_product_stock.add_subplot(111)
ax_product_stock.bar(sorted_product_names, sorted_product_stock, color='skyblue')
ax_product_stock.set_xlabel('Product Name', fontsize=12)  # Adjust font size
ax_product_stock.set_ylabel('Stock')
ax_product_stock.set_title('Product Stock Levels')
ax_product_stock.set_xticklabels(sorted_product_names, rotation=45, fontsize=8)  # Adjust rotation angle and font size

canvas_product_stock = FigureCanvasTkAgg(fig_product_stock, master=window)
canvas_product_stock.draw()
canvas_product_stock.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


window.mainloop()