from flask import Flask, render_template, request, redirect
import shortuuid

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.before_first_request
def create_table():
    db.create_all()

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longUrl = db.Column(db.String(500), unique=True, nullable=False)
    shortUrl = db.Column(db.String(10), unique=True, nullable=False)

    
    def __repr__(self):
        longUrl = self.longUrl 
        shortUrl = self.shortUrl 
    

def init_db():
    db.create_all()

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        requestUrl = request.form['URL']
        try:
            existing = Website.query.filter_by(longUrl=requestUrl).first()
            if existing.longUrl:
                return render_template("home.html", shortUrl=existing.shortUrl)
        except:
            return ("<h1>Please enter a URL</h1>")
        shortUrl = shortuuid.uuid()[:10]
        site = Website(longUrl=requestUrl, shortUrl=shortUrl)
        print(site.longUrl)
        print(site.shortUrl)
        db.session.add(site)
        db.session.commit()
        return render_template("home.html", shortUrl=shortUrl)
        

@app.route('/<string:shortUrl>', methods=["GET"])
def lengthen(shortUrl):
    site = Website.query.filter_by(shortUrl=shortUrl).first()
    longUrl = site.longUrl
    splitUrl = longUrl.split(":")
    print (splitUrl)
    if splitUrl[0] != "https" and splitUrl[0] != "http" :
        longUrl = "http://" + longUrl
        print(longUrl)

    return redirect(longUrl)
