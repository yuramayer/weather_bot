"""Main web app module"""

from flask import Flask, render_template
from weather import get_weather

app = Flask(__name__)


@app.route("/")
def home():
    """Root web page flask func"""
    emoji, label = get_weather()
    return render_template("index.html", emoji=emoji, label=label)


if __name__ == "__main__":
    app.run(debug=True)
