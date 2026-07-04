from flask import Flask, render_template, request, redirect, url_for, flash 
import sqlite3
import os

connection = sqlite3.connect("expense_tracker.db", check_same_thread=False)
cursor = connection.cursor()


# Creates expenses table if it doesn't already exist
def create_table():

    cursor.execute("""
    CREATE TABLE If NOT EXISTS expenses(
        id INTEGER PRIMARY KEY,
        name TEXT,
        cost REAL,
        category TEXT,
        date TEXT
        )
    """)

    # Retrieve information about the existing table columns
    cursor.execute("PRAGMA table_info(expenses)")
    columns = cursor.fetchall()

    # Extract only the column names
    column_names = [column[1] for column in columns]

    # Update older databases that do not have the date column
    if "date" not in column_names:
        cursor.execute(
            """
            ALTER TABLE expenses
            ADD COLUMN date TEXT
            """
        )
    connection.commit()

create_table() 

# Create Flask application
app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "development-secret-key"
)

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

# About page route
@app.route("/about")
def about():
    return render_template("about.html")

# Add expense page route
@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        # Retrieve submitted form data
        expense_name = request.form.get("expense_name", "").strip()
        cost_input = request.form.get("cost", "").strip()
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()

        # Stop if any field is empty 
        if not expense_name or not cost_input or not category or not date:
            return render_template(
                "add_expense.html",
                error="All fields required."
            )

        # Safely convert the cost from text to a decimal number
        try:
            cost = float(cost_input)
        except ValueError:
            return render_template(
                "add_expense.html", 
                error="Cost must be a valid number."
            )
        
        # Check that cost is positive
        if cost <= 0:
            return render_template(
                "add_expense.html",
                error="Cost must be greater than zero."
                )
        
        # Save the new expense to the database
        cursor.execute(
            """
            INSERT INTO expenses
            (name, cost, category, date)
            VALUES (?, ?, ?, ?)
            """,
            (expense_name, cost, category, date)
        )

        connection.commit()

        flash("Expense added successfully.")

        # After adding, send user to the view expenses page
        return redirect(url_for("view_expenses"))

    # If the user visits /add-expense normally, show the form
    return render_template("add_expense.html")

# View expenses page route
@app.route("/view-expenses")
def view_expenses():

    # URL values
    category = request.args.get("category", "").strip()
    search = request.args.get("search", "").strip()
    sort = request.args.get("sort", "").strip()
    month = request.args.get("month", "").strip()

    # Start buidling the SQL query
    query = "SELECT * FROM expenses"
    conditions = []
    parameters = []

    if category:
        # Displays expenses based on category entered
        conditions.append("category LIKE ?")
        parameters.append(f"%{category}%")
    
    if search:
        # Searches and displays the expense entered
        conditions.append("name LIKE ?")
        parameters.append(f"%{search}%")

    if month:
        # Filters expenses by month
        conditions.append("strftime('%Y-%m', date) = ?")
        parameters.append(month)
    
    # Add all active filters to the query
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if sort == "cost_asc":
        # Sort lowest to highest
        query += " ORDER BY cost ASC"

    elif sort == "cost_desc":
        # Sort highest to lowest
        query += " ORDER BY cost DESC"

    elif sort == "date_asc":
        # Sort oldest to newest
        query += " ORDER BY date ASC"
    
    elif sort == "date_desc":
        # Sort newest to oldest
        query += " ORDER BY date DESC"

    # Execute the completed query once
    cursor.execute(query, parameters)
    expenses = cursor.fetchall()

    # Start a seperate query to total the currently displayed expenses
    total_query = "SELECT SUM(cost) FROM expenses"

    # Apply the same filters used by the expense list
    if conditions:
        total_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(total_query, parameters)
    result = cursor.fetchone()

    # Display zero when no matching expenses exist
    total = result[0] if result[0] is not None else 0

    # Calculate total spending for each category
    cursor.execute(
        """
        SELECT category, SUM(cost)
        FROM expenses
        GROUP BY category
        """
    )

    category_totals = cursor.fetchall()

    # Calculate total spending for each month
    cursor.execute(
        """
        SELECT strftime('%Y-%m', date), SUM(cost)
        FROM expenses
        WHERE date IS NOT NULL AND date != ''
        GROUP BY strftime('%Y-%m', date)
        ORDER BY strftime('%Y-%m', date) ASC
        """
    )

    monthly_totals = cursor.fetchall()

    

    # Send both the expense records and total spending to HTML
    return render_template(
        "view_expenses.html", 
        expenses=expenses, 
        total=total, 
        category_totals=category_totals, 
        monthly_totals=monthly_totals,
        category=category,
        search=search,
        month=month,
        sort=sort
    )

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

    flash("Expense deleted successfully.")

    return redirect(url_for("view_expenses"))

# Edit expense page route
@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):

    # Handle the submitted edit form
    if request.method == "POST":
        # Retrieve submitted form data
        expense_name = request.form.get("expense_name", "").strip()
        cost_input = request.form.get("cost", "").strip()
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()

        # Stop if any field is empty 
        if not expense_name or not cost_input or not category or not date:
            return render_template(
                "edit_expense.html",
                error="All fields required.",
                expense=(expense_id, expense_name, cost_input, category, date)
            )

        # Safely convert the cost from text to a decimal number
        try:
            cost = float(cost_input)
        except ValueError:
            return render_template(
                "edit_expense.html",
                error="Cost must be a valid number.",
                expense=(expense_id, expense_name, cost_input, category, date)
                )
        
        # Check that cost is positive
        if cost <= 0:
            return render_template(
                "edit_expense.html",
                error="Cost must be greater than zero.",
                expense=(expense_id, expense_name, cost_input, category, date)
                )

        cursor.execute(
            """
            UPDATE expenses
            SET 
                name = ?,
                cost = ?,
                category = ?,
                date = ?
            WHERE id = ?
            """,
            (expense_name, cost, category, date, expense_id)
        )

        connection.commit()

        flash("Expense updated successfully.")

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

