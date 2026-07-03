# Expense Tracker

## Description

The Expense Tracker is a Flask web application designed to help users record, organize, and review their spending. Users can add new expenses, view existing records, update expense information, and delete expenses they no longer need.

The application also allows users to search and filter expenses by name, category, and month. Expenses can be sorted by cost or date, and the dashboard provides spending totals by category and month to make financial activity easier to understand.

## Features

* Add, view, edit, and delete expenses
* Search expenses by name
* Filter expenses by category and month
* Sort expenses by cost and date
* Calculate totals for filtered expenses
* Display spending summaries by category and month
* Validate submitted form data
* Display success, error, and no-results messages
* Responsive layout for desktop and mobile screens
* Delete confirmation to prevent accidental removal

## Technologies Used

* Python
* Flask
* SQLite
* HTML
* CSS
* Jinja
* Git and GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/DeviWilk3747/expense-tracker-flask.git
```

Enter the project directory:

```bash
cd expense-tracker-flask
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Running the Application

Start the Flask application:

```bash
python expense_tracker_flask.py
```

Then open the following address in a browser:

```text
http://127.0.0.1:5000
```

## Project Structure

```text
expense-tracker-flask/
├── static/
│   └── styles.css
├── templates/
│   ├── about.html
│   ├── add_expense.html
│   ├── base.html
│   ├── edit_expense.html
│   ├── index.html
│   └── view_expenses.html
├── .gitignore
├── expense_tracker_flask.py
├── README.md
└── requirements.txt
```

The SQLite database is created locally when the application runs and is excluded from Git tracking.

## Skills Demonstrated

* Flask routing and request handling
* SQLite database operations
* Create, read, update, and delete operations
* Parameterized SQL queries
* Dynamic searching, filtering, and sorting
* Server-side and browser-side form validation
* Jinja template inheritance
* Responsive CSS layouts
* Git and GitHub version control

## Future Improvements

* Add user accounts and authentication
* Allow each user to manage a private expense history
* Add spending budgets and budget alerts
* Display charts for monthly and category spending
* Export expense records to CSV
* Add pagination for larger expense histories
* Deploy the application online
* Use environment variables for configuration and secret keys
* Create automated tests for Flask routes and database operations
