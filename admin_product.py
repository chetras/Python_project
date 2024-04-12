import tkinter as tk
from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title("Product Management System")
window.geometry('925x680+300+200')

# Custom Font for Buttons
button_font = ("Arial", 10)  # Custom font for buttons

# Button Click Functions
def products_click():
    print("Products button clicked")

def customers_click():
    print("Customers button clicked")

def manage_click():
    print("Manage button clicked")

def exit_click():
    window.destroy()

# Frame for Buttons
button_frame = tk.Frame(window)
button_frame.pack(side="top", fill="x")

# Buttons for Products, Customers, Manage, Exit
products_button = tk.Button(button_frame, text="Products", font=button_font, command=products_click, width=10)
products_button.pack(side="left")

customers_button = tk.Button(button_frame, text="Customers", font=button_font, command=customers_click, width=10)
customers_button.pack(side="left")

manage_button = tk.Button(button_frame, text="Manage", font=button_font, command=manage_click, width=10)
manage_button.pack(side="left")

signout_button = tk.Button(button_frame, text="Sign Out", font=button_font, command=exit_click, width=10)
signout_button.pack(side="left")

# Icon Area
icon_label = tk.Label(window, text="(icon)", font=("Arial", 20))
icon_label.pack(side="left", padx=10)

# Form Fields
form_frame = tk.Frame(window)
form_frame.pack(side="left", padx=10)

form_labels = ["Pro. #", "Pro. Name", "Type", "Price", "Stock"]
form_entries = []

for label_text in form_labels:
    label = tk.Label(form_frame, text=label_text)
    label.pack(anchor="w")
    entry = tk.Entry(form_frame)
    entry.pack(anchor="w")
    form_entries.append(entry)

# Buttons
buttons_frame = tk.Frame(window)
buttons_frame.pack(side="left", padx=10)

buttons = ["Add", "Update", "Delete", "Show/All"]

for button_text in buttons:
    button = tk.Button(buttons_frame, text=button_text, width=10)
    button.pack(fill="x", padx=5, pady=5)

# Table
table_frame = tk.Frame(window)
table_frame.pack(side="right", padx=10, fill="both", expand=True)

columns = ("#", "Name", "Type", "Price", "Stock")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=100)
table.pack(side="left", fill="both", expand=True)

# Insert sample data into the table
data = [
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("1", "Product A", "Type A", "$10.00", "100"),
    ("2", "Product B", "Type B", "$15.00", "150"),
    ("3", "Product C", "Type C", "$20.00", "200"),
    ("4", "Product D", "Type D", "$25.00", "250")
]

for row in data:
    table.insert("", "end", values=row)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=scrollbar.set)

window.mainloop()
