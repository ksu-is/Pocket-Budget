import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# -----------------------------
# Database setup
# -----------------------------
conn = sqlite3.connect("pocketbudget.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_name TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()

# -----------------------------
# Functions
# -----------------------------
def add_expense():
    expense_name = entry_name.get().strip()
    category = category_var.get().strip()
    amount = entry_amount.get().strip()
    date = entry_date.get().strip()

    if not expense_name or not category or not amount or not date:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        amount = float(amount)
        if amount <= 0:
            messagebox.showerror("Input Error", "Amount must be greater than zero.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
        return

    cursor.execute(
        "INSERT INTO expenses (expense_name, category, amount, date) VALUES (?, ?, ?, ?)",
        (expense_name, category, amount, date)
    )
    conn.commit()

    messagebox.showinfo("Success", "Expense added successfully.")

    entry_name.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    category_var.set("Food")

    refresh_expenses()

def refresh_expenses():
    listbox_expenses.delete(0, tk.END)
    cursor.execute("SELECT expense_name, category, amount, date FROM expenses")
    rows = cursor.fetchall()

    total_spent = 0
    for row in rows:
        expense_name, category, amount, date = row
        total_spent += amount
        listbox_expenses.insert(
            tk.END,
            f"{expense_name} | {category} | ${amount:.2f} | {date}"
        )

    label_total.config(text=f"Total Spent: ${total_spent:.2f}")

# -----------------------------
# Tkinter window
# -----------------------------
root = tk.Tk()
root.title("PocketBudget")
root.geometry("500x500")

title_label = tk.Label(root, text="PocketBudget", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

subtitle_label = tk.Label(root, text="Track your spending and stay within budget")
subtitle_label.pack(pady=5)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Expense Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_name = tk.Entry(frame_inputs, width=25)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Category:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
category_var = tk.StringVar(value="Food")
category_menu = ttk.Combobox(
    frame_inputs,
    textvariable=category_var,
    values=["Food", "Transportation", "Entertainment", "School", "Bills", "Personal", "Subscriptions", "Other"],
    state="readonly",
    width=22
)
category_menu.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Amount:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_amount = tk.Entry(frame_inputs, width=25)
entry_amount.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
entry_date = tk.Entry(frame_inputs, width=25)
entry_date.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(root, text="Add Expense", command=add_expense)
btn_add.pack(pady=10)

label_total = tk.Label(root, text="Total Spent: $0.00", font=("Arial", 12, "bold"))
label_total.pack(pady=5)

tk.Label(root, text="Recent Expenses").pack(pady=5)
listbox_expenses = tk.Listbox(root, width=60, height=12)
listbox_expenses.pack(pady=10)

refresh_expenses()

root.mainloop()

conn.close()