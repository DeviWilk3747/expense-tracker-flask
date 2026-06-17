from flask import Flask, render_template, request, redirect, url_for 
import sqlite3

connection = sqlite3.connect("expense_tracker.db", check_same_thread=False)
cursor = connection.cursor()


# Creates expenses table if it doesn't already exist
def create_table():

    cursor.execute("""
    CREATE TABLE If NOT EXISTS expenses(
        id INTEGER PRIMARY KEY,
        name TEXT,
        cost REAL,
        category TEXT
        )
    """)
    connection.commit()

create_table() 

# Create Flask application
app = Flask(__name__)

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

# About page route
@app.route("/about")
def about():
    return "About Page"

# Add expense page route
@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        # Retrieve submitted form data
        expense_name = request.form["expense_name"]
        cost = float(request.form["cost"])
        category = request.form["category"]

        # Save the new expense to the database
        cursor.execute(
            """
            INSERT INTO expenses
            (name, cost, category)
            VALUES (?, ?, ?)
            """,
            (expense_name, cost, category)
        )

        connection.commit()

        # After adding, send user to the view expenses page
        return redirect(url_for("view_expenses"))

    # If the user visits /add-expense normally, show the form
    return render_template("add_expense.html")

# View expenses page route
@app.route("/view-expenses")
def view_expenses():

    category = request.args.get("category")

    if category:

        # Displays expenses based on category entered
        cursor.execute(
            """
            SELECT * FROM expenses
            WHERE category = ?
            """,
            (category,)
        )
    else:
        
        # Displaays all expenses from the database
        cursor.execute("SELECT * FROM expenses")

    expenses = cursor.fetchall()

    if category:
         # Calculates total expenses from inserted category
         cursor.execute(
            """
            SELECT SUM(cost) FROM expenses
            WHERE category = ?
            """,
            (category,)
         )
    else:
        # Calculates total cost of all expenses
        cursor.execute("SELECT SUM(cost) FROM expenses")
  
    result = cursor.fetchone()

    # If there are no expenses yet
    total = result[0] if result[0] is not None else 0

    # Send both the expense records and total spending to HTML
    return render_template("view_expenses.html", expenses=expenses, total=total)

# Delete expense route
@app.route("/delete-expense/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):

    # Deletes expense
    cursor.execute(
        """
        DELETE FROM expenses 
        WHERE id = ?
        """,
        (expense_id,)
        )

    connection.commit()
    return redirect(url_for("view_expenses"))

# Edit expense page route
@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):

    # Handle the submitted edit form
    if request.method == "POST":
            expense_name = request.form["expense_name"]
            cost = float(request.form["cost"])
            category = request.form["category"]

            cursor.execute(
                """
                UPDATE expenses
                SET 
                    name = ?,
                    cost = ?,
                    category = ?
                WHERE id = ?
                """,
                (expense_name, cost, category, expense_id)
            )

            connection.commit()

            return redirect(url_for("view_expenses"))
    
    # A GET request retrieves the current expense for the form
    cursor.execute(
        """
        SELECT * FROM expenses
        WHERE id = ?
        """,
        (expense_id,)
    )

    expense = cursor.fetchone()
    

    # Handles an ID that does not exist
    if expense is None:
        return "Expense not found", 404
    
    # Send the selected expense to the edit form
    return render_template("edit_expense.html", expense=expense)

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)

