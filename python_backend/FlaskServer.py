from flask import Flask
import

app = Flask(__name__)

@app.route("/address/<address>")
def hello_world(address):
    return f"<p>{address}</p>"
