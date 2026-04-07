from flask import Flask, render_template, request, send_file, jsonify
import io
import base64
import qrcode

app = Flask(__name__)


# This function creates a QR code image from the user's input.
def build_qr_image(user_input):
    qr = qrcode.QRCode(
        version=None,
        box_size=10,
        border=4
    )
    qr.add_data(user_input)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


# This function converts the QR image into base64 so it can be displayed on the webpage.
def build_qr_base64(user_input):
    img = build_qr_image(user_input)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# This checks if the request came from JavaScript (AJAX) instead of a normal form submit.
def is_ajax_request(req):
    return req.headers.get("X-Requested-With") == "XMLHttpRequest"


# This loads the main page when the user first opens the site.
@app.get("/")
def home():
    return render_template("index.html")


# This handles generating the QR code after the user submits input.
@app.post("/generate")
def generate():
    user_input = request.form.get("data", "").strip()

    # This checks if the input is empty and returns an error if it is.
    if not user_input:
        if is_ajax_request(request):
            return jsonify({
                "success": False,
                "error": "Please enter text or a URL before generating a QR code."
            }), 400

        return render_template(
            "index.html",
            error="Please enter text or a URL before generating a QR code."
        )

    # This checks if the input is too long and stops it if over the limit.
    if len(user_input) > 1000:
        if is_ajax_request(request):
            return jsonify({
                "success": False,
                "error": "Input is too long. Please keep it under 1000 characters."
            }), 400

        return render_template(
            "index.html",
            error="Input is too long. Please keep it under 1000 characters.",
            submitted_text=user_input
        )

    # This tries to generate the QR code and return it to the user.
    try:
        img_b64 = build_qr_base64(user_input)

        if is_ajax_request(request):
            return jsonify({
                "success": True,
                "message": "QR code generated successfully.",
                "qr_data": img_b64,
                "submitted_text": user_input
            })

        return render_template(
            "index.html",
            qr_data=img_b64,
            submitted_text=user_input,
            message="QR code generated successfully."
        )

    # This catches any errors during generation and shows a message.
    except Exception:
        if is_ajax_request(request):
            return jsonify({
                "success": False,
                "error": "Something went wrong while generating the QR code. Please try again."
            }), 500

        return render_template(
            "index.html",
            error="Something went wrong while generating the QR code. Please try again."
        )


# This allows the user to download the generated QR code as an image file.
@app.get("/download")
def download_qr():
    user_input = request.args.get("data", "").strip()

    # This checks if there is anything to download first.
    if not user_input:
        return render_template(
            "index.html",
            error="There is no QR code to download. Generate one first"
        )

    # This generates the image again and sends it as a downloadable file.
    try:
        img = build_qr_image(user_input)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="image/png",
            as_attachment=True,
            download_name="qr_code.png"
        )
    except Exception:
        return render_template(
            "index.html",
            error="Something went wrong while downloading the QR code. Please try again."
        )


# This handles server errors (like if the backend stops working).
@app.errorhandler(500)
def handle_server_error(error):
    if is_ajax_request(request):
        return jsonify({
            "success": False,
            "error": "Unable to connect to the server right now. Please try again."
        }), 500

    return render_template(
        "index.html",
        error="Unable to connect to the server right now. Please try again."
    ), 500


# This runs the Flask app when you start the file.
if __name__ == "__main__":
    app.run(debug=True)
