from flask import Flask, render_template, request

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/generate")
def generate():
    user_input = request.form.get("data", "").strip()

    if not user_input:
        return render_template("index.html", error="Please enter text or a URL.")

    # Sprint 1: prove frontend -> backend works
    return render_template("index.html", message=f"Received: {user_input}")

if __name__ == "__main__":
    app.run(debug=True)