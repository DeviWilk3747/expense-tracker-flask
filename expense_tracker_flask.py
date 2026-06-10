from flask import Flask, render_template

# Create Flask application
app = Flask(__name__)

# Home page route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "About Page"

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)

