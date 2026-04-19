# main application entry point
# sets up flask server, enables cors, and registers api routes

from flask import Flask, send_from_directory
from flask_cors import CORS
from timetable_routes import timetable_bp
import os

# create the flask app instance
app = Flask(__name__)

# enable cross-origin requests so the frontend can call the api
CORS(app)

# register all timetable api routes under the /api prefix
app.register_blueprint(timetable_bp, url_prefix="/api")


# serve the frontend html when someone visits the root url
@app.route("/")
def serve_index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")


# start the server on port 5000 when this file is run directly
if __name__ == "__main__":
    app.run(debug=True, port=5000)
