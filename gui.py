import sqlite3
import tkinter as tk
from tkinter import ttk

def enter_expense():
    date = date_entry.get()
    description = description_entry.get()
    category_choice = category_combobox.get()
    if category_choice == "Create a new Category":
        category = new_category_entry.get()
    else:
        category = category_choice
    price = price_entry.get()
    cur.execute("INSERT INTO expenses (Date,description,category,price) VALUES (?,?,?,?)", (date, description, category, price))
    conn.commit()
    update_expenses()

def view_expenses():
    view_choice = view_combobox.get()
    if view_choice == "View all Expenses":
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        for expense in expenses:
            print(expense)
    elif view_choice == "View monthly expenses by category":
        month = month_entry.get()
        year = year_entry.get()
        cur.execute("""SELECT category ,SUM(price) FROM expenses 
                       WHERE strftime('%m',Date)=? AND strftime('%Y',Date)=? GROUP BY category""", (month, year))
        expenses = cur.fetchall()
        for expense in expenses:
            print(f"Category:{expense[0]},Total:{expense[1]}")

def update_expenses():
    expenses_tree.delete(*expenses_tree.get_children())
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    for expense in expenses:
        expenses_tree.insert("", "end", values=expense)

# Create SQLite database connection
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

# Create GUI window
root = tk.Tk()
root.title("Expense Tracker")

# Create and place widgets in the GUI
date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=0, column=0, padx=10, pady=10)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=10, pady=10)

description_label = tk.Label(root, text="Description:")
description_label.grid(row=1, column=0, padx=10, pady=10)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1, padx=10, pady=10)

cur.execute("SELECT DISTINCT category FROM expenses")
categories = [category[0] for category in cur.fetchall()]
categories.append("Create a new Category")
category_label = tk.Label(root, text="Category:")
category_label.grid(row=2, column=0, padx=10, pady=10)
category_combobox = ttk.Combobox(root, values=categories)
category_combobox.grid(row=2, column=1, padx=10, pady=10)
new_category_entry = tk.Entry(root)

price_label = tk.Label(root, text="Price:")
price_label.grid(row=3, column=0, padx=10, pady=10)
price_entry = tk.Entry(root)
price_entry.grid(row=3, column=1, padx=10, pady=10)

enter_button = tk.Button(root, text="Enter Expense", command=enter_expense)
enter_button.grid(row=4, column=0, columnspan=2, pady=10)

view_label = tk.Label(root, text="View Expenses:")
view_label.grid(row=5, column=0, padx=10, pady=10)
view_choices = ["View all Expenses", "View monthly expenses by category"]
view_combobox = ttk.Combobox(root, values=view_choices)
view_combobox.grid(row=5, column=1, padx=10, pady=10)

view_button = tk.Button(root, text="View", command=view_expenses)
view_button.grid(row=6, column=0, columnspan=2, pady=10)

month_label = tk.Label(root, text="Month (MM):")
month_label.grid(row=7, column=0, padx=10, pady=10)
month_entry = tk.Entry(root)
month_entry.grid(row=7, column=1, padx=10, pady=10)

year_label = tk.Label(root, text="Year (YYYY):")
year_label.grid(row=8, column=0, padx=10, pady=10)
year_entry = tk.Entry(root)
year_entry.grid(row=8, column=1, padx=10, pady=10)

expenses_tree = ttk.Treeview(root, columns=("Date", "Description", "Category", "Price"), show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Description", text="Description")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Price", text="Price")
expenses_tree.grid(row=9, column=0, columnspan=2, pady=10)

update_expenses()

# Start the GUI event loop
root.mainloop()

# Close the database connection
conn.close()
