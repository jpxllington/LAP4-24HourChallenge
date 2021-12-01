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

    # def __repr__(self):
    #     return f"UrlModel('{self.longUrl}', '{self.shortUrl}')"
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
    # site = Website.query.all()
    print(f"This was found in the db {site.longUrl}")
    # longUrl = site.longUrl
    return redirect(site.longUrl)

# from flask import Flask, request, render_template, redirect
# from utils import *
# app = Flask(__name__)
# @app.route('/', methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         short_name = request.form.get('name')
#         url = request.form.get('url')
#         if 'http' not in url:
#             url = f'http://{url}'
#             if valid_url(url):      
#                 if name_available(short_name) is None:
#                     add_url(short_name, url)
#                     return render_template("success.html", short_name=short_name)
#                 else:
#                     return render_template('index.html', msg='Short name not available')
#         else:
#             return render_template('index.html', msg='Invalid url')
#         return render_template('index.html')

# @app.route('/<path:short_name>')
# def redirect_url(short_name):
#     url = get_url(short_name)
#     if url is None:
#         return "<h2 style='color:red'> Invalid URL </h2>"
#     return redirect(url.url)