from aicybernewssummary import AICyberNewsSummary
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        get_summary = AICyberNewsSummary(user_input)
        response = get_summary.summary()
        # Simulate sending user_input to the backend (replace with your actual logic)
        #response = f"You entered: {user_input}"
        return render_template("index.html", user_input=user_input, response=response)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
