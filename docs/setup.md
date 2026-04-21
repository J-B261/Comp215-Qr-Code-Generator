# Development Setup

This project was built as a QR Code Generator  using Python, Flask, HTML, and CSS. It allows a user to enter text or a URL, send it to the backend, generate a QR code, and display the result on the webpage.

## Tools Used
- Windows 11
- Visual Studio Code
- Python 3
- Flask
- qrcode library

## Project Structure
    project-folder/
    ├── app.py
    ├── static/
    │   └── style.css
    └── templates/
        └── index.html

## Setup Instructions
1. Install Python 3 and make sure it is added to PATH.
2. Install Visual Studio Code.
3. Open the project folder in VS Code.
4. Open the terminal and create a virtual environment:

```bash
- `python -m venv venv` creates a virtual environment for the project.
- `venv\Scripts\activate` activates the virtual environment.
- `pip install flask qrcode[pil] pillow` installs the required project libraries.
- `python app.py` runs the Flask application.
- `http://127.0.0.1:5000` is the local address used to open the project in a browser.
