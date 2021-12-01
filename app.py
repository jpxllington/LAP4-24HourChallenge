from flask import Flask, render_template, request, redirect
import shortuuid
from werkzeug import werkzeug
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////website.db'
db = SQLAlchemy(app)

@app.before_first_request
def create_table():
    db.create_all()

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longUrl = db.Column(db.String(500), unique=True, nullable=False)
    shortUrl = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, longUrl, shortUrl):
        self.longUrl = longUrl
        self.shortUrl = shortUrl
    

@app.route('/', methods=["GET","POST"])
def index():
    if request.method== "GET":
        return render_template("home.html")
    elif request.method == "POST":
        requestUrl = request.get_json()
        shortUrl = shortuuid.uuid()[:10]
        site = Website(longUrl=requestUrl, shortUrl=shortUrl)
        return render_template("home.html", shortUrl=shortUrl)
        


