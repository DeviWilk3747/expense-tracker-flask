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
        cost REAL
        
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
@app.route("/add-expense", methods=["POST"])
def add_expense():

    # Requests information from the webpage
    expense_name = request.form["expense_name"]
    cost = float(request.form["cost"])

    print(f"Expense: {expense_name}")
    print(f"Cost: {cost}")
    # Adds the information to expense_tracker database
    cursor.execute(
    """
    INSERT INTO expenses
    (name, cost)
    VALUES (?, ?)
    """,
    (expense_name, cost)
    )

    connection.commit()
    cursor.execute("SELECT * FROM expenses")
    

    # Redirects user to the home page
    return redirect(url_for("home"))

# View expenses page route
@app.route("/view-expenses")
def view_expenses():

    # Retrieve all expense records from the database
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    # Calculaate total cost of all expenses
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

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)

