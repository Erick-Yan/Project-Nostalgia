import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for, copy_current_request_context
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from functions import login_required, date_conversion, allowed_file, make_unique
import datetime

import logging
import logging.handlers

app = Flask(__name__)

IMAGE_UPLOADS = '/home/Erick3/mysite/static/uploads/images'
MUSIC_UPLOADS = '/home/Erick3/mysite/static/uploads/music'
ALLOWED_EXTENSIONS = {'mp3', 'png', 'jpg', 'jpeg'}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['IMAGE_UPLOADS'] = IMAGE_UPLOADS
app.config['MUSIC_UPLOADS'] = MUSIC_UPLOADS

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Erick3",
    password="33ey9851001",
    hostname="Erick3.mysql.pythonanywhere-services.com",
    databasename="Erick3$moments"
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Users(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    hash = db.Column(db.Text)
    last_name = db.Column(db.Text)
    first_name = db.Column(db.Text)

class Moments(db.Model):

    __tablename__ = "moments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text)
    title = db.Column(db.Text)
    date = db.Column(db.Text)
    location = db.Column(db.Text)
    music = db.Column(db.Text)
    entry = db.Column(db.Text)
    photo1 = db.Column(db.Text)
    photo2 = db.Column(db.Text)
    photo3 = db.Column(db.Text)
    photo4 = db.Column(db.Text)
    photo5 = db.Column(db.Text)
    photo6 = db.Column(db.Text)
    photo7 = db.Column(db.Text)
    photo8 = db.Column(db.Text)
    photo9 = db.Column(db.Text)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == 'GET':
        return render_template("register.html")
    else:
        reg_username = request.form.get("username")
        reg_password = request.form.get("password")
        reg_password_again = request.form.get("password_again")
        reg_lastname = request.form.get("last_name")
        reg_firstname = request.form.get("first_name")

        if not reg_username:
            flash("Must Include Username")
            return render_template("register.html")

        if not reg_password:
            flash("Must Include Password")
            return render_template("register.html")

        if not reg_password_again:
            flash("Must Include Confirmation")
            return render_template("register.html")

        if not reg_lastname:
            flash("Must Include Last Name")
            return render_template("register.html")

        if not reg_firstname:
            flash("Must Include First Name")
            return render_template("register.html")

        if reg_password != reg_password_again:
            flash("Passwords Must Match")
            return render_template("register.html")

        rows = db.engine.execute("SELECT * FROM users WHERE username = %s;", reg_username)
        rows = rows.fetchall()
        if len(rows) == 1:
            flash("Username Already Exists")
            return render_template("register.html")

        reg_user = db.engine.execute("INSERT INTO users (username, hash, last_name, first_name) VALUES (%s, %s, %s, %s)", reg_username, generate_password_hash(reg_password, method='pbkdf2:sha256', salt_length=8), reg_lastname, reg_firstname)
        rows2 = db.engine.execute("SELECT * FROM users WHERE username = %s;", reg_username)
        rows2 = rows2.fetchall()

        session["user_id"] = rows2[0]['id']
        flash(f"You have Registered as {reg_username}!")
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must Include Username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must Include Password")
            return render_template("login.html")

        # Query database for username
        rows = db.engine.execute("SELECT * FROM users WHERE username = %s",
                          request.form.get("username"))
        rows = rows.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Incorrect Username/Password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash(f"Welcome back {rows[0]['first_name']}!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/add", methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template("add.html")
    else:
        photos_save = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        music_file = ''
        music = request.files['music']
        photos = request.files.getlist('photos[]')

        '''if music.filename == '':
            flash('No selected file')
            return redirect(request.url)
        for i in photos:
            if i.filename == '':
                flash('Must Include Photos')
                return redirect(request.url)'''

        title = request.form.get('title')
        date = request.form.get('date')
        location = request.form.get('location')
        entry = request.form.get('entry')

        row = db.engine.execute("SELECT * FROM users WHERE id = %s", session['user_id'])
        row = row.fetchall()
        username = row[0]['username']
        title_check = db.engine.execute("SELECT * FROM moments WHERE username = %s AND title = %s", username, title)
        title_check = title_check.fetchall()

        if not title:
            flash('Must Include Title')
            return render_template("add.html")
        if not date:
            flash('Must Include Date')
            return render_template("add.html")
        if not location:
            flash('Must Include Location')
            return render_template("add.html")
        if not entry:
            flash('Must Include Entry')
            return render_template("add.html")
        if len(title_check) == 1:
            flash('Find A Unique Title That You Have Not Used')
            return render_template("add.html")

        date = date_conversion(date)

        if music and allowed_file(music.filename):
            filename = secure_filename(music.filename)
            filename = make_unique(filename)
            music_file = filename
            if filename[-4:] == ".mp3":
                music.save(os.path.join(app.config['MUSIC_UPLOADS'], filename))
            else:
                flash("Must Select MP3 File")
                return render_template("add.html")
        for i in photos:
            if i and allowed_file(i.filename):
                filename = secure_filename(i.filename)
                filename = make_unique(filename)
                filename = filename.replace("_", "")
                photos_save[photos.index(i)] = filename
                print(filename)
                i.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))

        daba = db.engine.execute("INSERT INTO moments (username, title, date, location, music, entry, photo1, photo2, photo3, photo4, photo5, photo6, photo7, photo8, photo9) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        username, title, date, location, music_file, entry,
        photos_save[0], photos_save[1], photos_save[2], photos_save[3], photos_save[4],
        photos_save[5], photos_save[6], photos_save[7], photos_save[8])

        flash('A New Memory Has Been Added!')
        return redirect('/')


@app.route("/timeline", methods=['GET', 'POST'])
@login_required
def timeline():
    timeline_list = []
    id_list = []
    photos_each = [0]
    if request.method == 'GET':
        '''{"title":[], "date":[], "location":[], "music":[], "entry":[], "photo1":[]
        "photo2":[], "photo3":[], "photo4":[], "photo5":[], "photo6":[], "photo7":[],"photo8":[], "photo9":[]}'''

        row1 = db.engine.execute("SELECT * FROM users WHERE id = %s", session['user_id'])
        row1 = row1.fetchall()
        username = row1[0]['username']
        row2 = db.engine.execute("SELECT title, date, location, music, entry, photo1, photo2, photo3, photo4, photo5, photo6, photo7, photo8, photo9 FROM moments WHERE username = %s ORDER BY date DESC", username)
        row2 = row2.fetchall()

        for i in row2:
            timeline_list.append(i)
            id_list.append('#' + i['title'])

        for i in row2:
            count = 0
            for j in [i['photo1'], i['photo2'], i['photo3'], i['photo4'], i['photo5'], i['photo6'], i['photo7'], i['photo8'], i['photo9']]:
                if j != " ":
                    count += 1
            photos_each.append(count)
        for i in range(len(photos_each)):
            if i > 0:
                photos_each[i] = photos_each[i] + photos_each[i - 1]


        print(photos_each)

        return render_template("timeline.html", id_list = id_list, timeline_list = timeline_list, length = len(timeline_list), photos_each=photos_each, length_photos = len(photos_each))
    else:
        title = request.form['submit_button']

        row1 = db.engine.execute("SELECT * FROM users WHERE id = %s", session['user_id'])
        row1 = row1.fetchall()
        username = row1[0]['username']
        row2 = db.engine.execute("SELECT title, date, location, music, entry, photo1, photo2, photo3, photo4, photo5, photo6, photo7, photo8, photo9 FROM moments WHERE username = %s AND title = %s ORDER BY date DESC", username, title)
        row2 = row2.fetchall()

        for i in [row2[0]['photo1'], row2[0]['photo2'], row2[0]['photo3'], row2[0]['photo4'], row2[0]['photo5'], row2[0]['photo6'], row2[0]['photo7'], row2[0]['photo8'], row2[0]['photo9'], row2[0]['music']]:
            if i != ' ':
                if i != row2[0]['music'] and os.path.isfile("static/uploads/images/{one}".format(one=i)):
                    os.remove(os.path.join(app.config['IMAGE_UPLOADS'], i))
                elif i == row2[0]['music'] and os.path.isfile("static/uploads/music/{one}".format(one=i)):
                    os.remove(os.path.join(app.config['MUSIC_UPLOADS'], i))
            else:
                continue


        daba = db.engine.execute("DELETE FROM moments WHERE username = %s AND title = %s", username, title)
        #daba = daba.fetchall()

        row3 = db.engine.execute("SELECT title, date, location, music, entry, photo1, photo2, photo3, photo4, photo5, photo6, photo7, photo8, photo9 FROM moments WHERE username = %s ORDER BY date DESC", username)
        row3 = row3.fetchall()

        for i in row3:
            timeline_list.append(i)
            id_list.append('#' + i['title'])

        for i in row3:
            count = 0
            for j in [i['photo1'], i['photo2'], i['photo3'], i['photo4'], i['photo5'], i['photo6'], i['photo7'], i['photo8'], i['photo9']]:
                if j != " ":
                    count += 1
            photos_each.append(count)
        for i in range(len(photos_each)):
            if i > 0:
                photos_each[i] = photos_each[i] + photos_each[i - 1]

        return render_template("timeline.html", id_list = id_list, timeline_list = timeline_list, length = len(timeline_list), photos_each=photos_each, length_photos = len(photos_each))



if __name__ == '__main__':
    app.run(debug=True)
