from flask import Flask, render_template, request, session
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__) 
app.secret_key = os.getenv("SECRET_KEY")  # Session Management
API_KEY = os.getenv("API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    response = None  # initialize to prevent UnboundLocalError
    current_time = datetime.now().strftime("%A, %d %B %Y • %I:%M %p")

    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        city = request.form["city"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)  

        if response.status_code == 200:
            data = response.json()
            weather = {
                "city": city.title(),
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"]
            }

            # Save city to history if not already there
            if city.title() not in session["history"]:
                session["history"].insert(0, city.title())
                if len(session["history"]) > 5:
                    session["history"].pop()

            session.modified = True

    return render_template("index.html", weather=weather, history=session["history"], current_time=current_time)

if __name__ == "__main__":
    app.run(debug=True)
