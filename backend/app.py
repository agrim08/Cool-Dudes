from flask import Flask,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db =  SQLAlchemy(app)
migrate = Migrate(app, db)

fronted_folder = os.path.join(os.getcwd(),"..","frontend" )
dist_folder = os.path.join(fronted_folder,"dist")

@app.route("/",defaults={"filename":""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = 'index.html'
    return send_from_directory(dist_folder,filename)

import routes

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001 , debug = True)