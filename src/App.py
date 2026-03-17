from flask import Flask, render_template, request
import io
import base64
import qrcode

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/generate")
def generate():
    user_input = request.form.get("data", "").strip()

    # Basic validation
    if not user_input:
        return render_template(
            "index.html",
            error="Please enter text or a URL before generating a QR code."
        )

    try:
        # Generate QR code
        qr = qrcode.QRCode(
            version=None,
            box_size=10,
            border=4
        )
        qr.add_data(user_input)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert image to base64 so it can be displayed in HTML
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return render_template(
            "index.html",
            qr_data=img_b64,
            submitted_text=user_input,
            message="QR code generated successfully."
        )

    except Exception:
        return render_template(
            "index.html",
            error="Something went wrong while generating the QR code. Please try again."
        )


@app.errorhandler(500)
def handle_server_error(error):
    return render_template(
        "index.html",
        error="Unable to connect to the server right now. Please try again."
    ), 500


if __name__ == "__main__":
    app.run(debug=True)
