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

cursor.execute("""
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY,
    budget_limit REAL NOT NULL
)
""")

conn.commit()

# This list stores the database IDs for expenses shown in the recent expenses list
expense_ids = []

# -----------------------------
# Functions
# -----------------------------
def get_budget_limit():
    cursor.execute("SELECT budget_limit FROM budget WHERE id = 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0.0


def set_budget_limit():
    budget_amount = entry_budget.get().strip()

    if not budget_amount:
        messagebox.showerror("Input Error", "Please enter a budget amount.")
        return

    try:
        budget_amount = float(budget_amount)
        if budget_amount <= 0:
            messagebox.showerror("Input Error", "Budget must be greater than zero.")
            return
    except ValueError:
        messagebox.showerror("Input Error", "Budget must be a number.")
        return

    cursor.execute("""
    INSERT OR REPLACE INTO budget (id, budget_limit)
    VALUES (1, ?)
    """, (budget_amount,))

    conn.commit()

    messagebox.showinfo("Success", "Budget limit updated successfully.")
    refresh_expenses()


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


def delete_expense():
    selected = listbox_expenses.curselection()

    if not selected:
        messagebox.showerror("Selection Error", "Please select an expense to delete.")
        return

    selected_index = selected[0]
    expense_id = expense_ids[selected_index]
    selected_expense = listbox_expenses.get(selected_index)

    confirm = messagebox.askyesno(
        "Delete Expense",
        f"Are you sure you want to delete this expense?\n\n{selected_expense}"
    )

    if confirm:
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()

        messagebox.showinfo("Success", "Expense deleted successfully.")
        refresh_expenses()


def refresh_expenses():
    listbox_expenses.delete(0, tk.END)
    listbox_category_totals.delete(0, tk.END)
    expense_ids.clear()

    cursor.execute("""
    SELECT id, expense_name, category, amount, date
    FROM expenses
    ORDER BY date DESC, id DESC
    """)
    rows = cursor.fetchall()

    total_spent = 0
    category_totals = {}

    for row in rows:
        expense_id, expense_name, category, amount, date = row

        expense_ids.append(expense_id)
        total_spent += amount

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

        listbox_expenses.insert(
            tk.END,
            f"{expense_name} | {category} | ${amount:.2f} | {date}"
        )

    if category_totals:
        for category, total in sorted(category_totals.items(), key=lambda item: item[1], reverse=True):
            listbox_category_totals.insert(tk.END, f"{category}: ${total:.2f}")
    else:
        listbox_category_totals.insert(tk.END, "No category totals yet.")

    budget_limit = get_budget_limit()
    remaining = budget_limit - total_spent

    label_total.config(text=f"Total Spent: ${total_spent:.2f}")
    label_budget.config(text=f"Budget Limit: ${budget_limit:.2f}")

    if budget_limit > 0:
        label_remaining.config(text=f"Remaining Budget: ${remaining:.2f}")

        if remaining < 0:
            label_remaining.config(fg="red")
            label_status.config(text="You are over budget!", fg="red")
        else:
            label_remaining.config(fg="green")
            label_status.config(text="You are within your budget.", fg="green")
    else:
        label_remaining.config(text="Remaining Budget: $0.00", fg="black")
        label_status.config(text="No budget limit set.", fg="black")


# -----------------------------
# Tkinter window
# -----------------------------
root = tk.Tk()
root.title("PocketBudget")
root.geometry("550x780")

title_label = tk.Label(root, text="PocketBudget", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

subtitle_label = tk.Label(root, text="Track your spending and stay within budget")
subtitle_label.pack(pady=5)

# -----------------------------
# Budget input section
# -----------------------------
frame_budget = tk.Frame(root)
frame_budget.pack(pady=10)

tk.Label(frame_budget, text="Budget Limit:").grid(row=0, column=0, sticky="e", padx=5, pady=5)

entry_budget = tk.Entry(frame_budget, width=20)
entry_budget.grid(row=0, column=1, padx=5, pady=5)

btn_budget = tk.Button(frame_budget, text="Set Budget", command=set_budget_limit)
btn_budget.grid(row=0, column=2, padx=5, pady=5)

# -----------------------------
# Expense input section
# -----------------------------
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
    values=[
        "Food",
        "Transportation",
        "Entertainment",
        "School",
        "Bills",
        "Personal",
        "Subscriptions",
        "Other"
    ],
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

label_feedback = tk.Label(root, text="", font=("Arial", 10, "bold"))
label_feedback.pack(pady=3)

# -----------------------------
# Spending summary
# -----------------------------
label_total = tk.Label(root, text="Total Spent: $0.00", font=("Arial", 12, "bold"))
label_total.pack(pady=3)

label_budget = tk.Label(root, text="Budget Limit: $0.00", font=("Arial", 12, "bold"))
label_budget.pack(pady=3)

label_remaining = tk.Label(root, text="Remaining Budget: $0.00", font=("Arial", 12, "bold"))
label_remaining.pack(pady=3)

label_status = tk.Label(root, text="No budget limit set.", font=("Arial", 11, "bold"))
label_status.pack(pady=3)

tk.Label(root, text="Spending by Category", font=("Arial", 11, "bold")).pack(pady=5)

listbox_category_totals = tk.Listbox(root, width=60, height=8)
listbox_category_totals.pack(pady=5)

tk.Label(root, text="Recent Expenses", font=("Arial", 11, "bold")).pack(pady=5)

listbox_expenses = tk.Listbox(root, width=60, height=10)
listbox_expenses.pack(pady=10)

btn_delete = tk.Button(root, text="Delete Selected Expense", command=delete_expense)
btn_delete.pack(pady=5)

# Load saved budget into input box
saved_budget = get_budget_limit()
if saved_budget > 0:
    entry_budget.insert(0, str(saved_budget))

refresh_expenses()

root.mainloop()

conn.close()