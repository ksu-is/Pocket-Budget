# PocketBudget

## Overview
PocketBudget is a Python-based budgeting and expense tracking application designed for students. The goal of the project is to help users record everyday spending, organize expenses into categories, and better understand where their money is going.

Many students live on a limited budget, but the real challenge is often keeping track of small purchases that add up over time. PocketBudget is meant to make those spending habits visible and easier to manage.

## Problem
Students often struggle to keep track of daily expenses such as food, transportation, subscriptions, and entertainment. Existing finance tools can feel too complex or are designed for long-term financial planning instead of simple day-to-day budgeting.

## Solution
PocketBudget provides a lightweight way for students to:
- add expenses
- assign expenses to categories
- view spending history
- track spending against a weekly or monthly budget
- see a summary of total spending by category

## Intended Users
The primary users are college students and other young adults managing limited income.

## Planned Features
- Add a new expense
- Assign expense categories
- Store expense records
- View expense history
- Track remaining budget
- Show spending summaries by category
- Display categories with the highest spending

## Tools and Technologies
- Python
- Tkinter for the graphical user interface
- SQLite for data storage

## Setup Instructions
- Make sure Python is installed on your computer.
- Download or clone this repository.
- Open the project folder in your code editor or terminal.
- Run the application with: python main.py

## Usage Instructions
1. Enter the name of the expense, such as `Lunch`, `Gas`, or `Textbook`.
2. Select a category from the dropdown menu.
3. Enter the amount of the expense.
4. Enter the date using the format `YYYY-MM-DD`.
5. Click **Add Expense** to save the expense.
6. Review the recent expenses list to see previously entered expenses.
7. Check the **Total Spent** amount to see how much has been recorded.

## Sprint 1 Goals
- Set up the project repository
- Create project documentation
- Research similar repositories
- Build an initial application structure
- Plan core features for development

## Sprint 2 Goals
- Improve expense input validation for amount and date fields
- Add a budget limit feature for users to enter a planned spending amount
- Display the remaining budget after expenses are added
- Add clearer success and error messages when users submit expenses
- Improve the recent expenses display so entries are easier to read
- Add category-based spending totals for better spending summaries
- Update README.md with clearer setup and usage instructions
- Test the app with multiple expenses across different categories

## Team
- Jack Hubbard

## Related Repositories
- https://github.com/happy-harsh/Expense-Tracker-python-GUI
- https://github.com/AbhayKumar-Proficient/Expense-Tracker-Python

## References
- https://docs.python.org/3/library/tkinter.html
- https://docs.python.org/3/library/sqlite3.html

# Related Repository Review

## Repository Reviewed
Expense Tracker Python GUI  
https://github.com/happy-harsh/Expense-Tracker-python-GUI

## What I learned
- Expense tracking apps can be kept simple and still be useful
- A GUI makes the project more practical for student users
- Category-based organization is important for seeing spending patterns

## Ideas useful for PocketBudget
- Simple expense entry form
- Clear display of past transactions
- Basic summaries of spending

## Notes
PocketBudget will focus more specifically on student budgeting, keeping the design lightweight and centered on weekly or monthly budget goals.
