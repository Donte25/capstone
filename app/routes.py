from app import app

from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from .forms import RegisterForm, LoginForm, SearchForm
from .models import db, User
from flask_socketio import SocketIO, send

import requests as r

socketio = SocketIO(app, cors_allowed_origins = '*')

@socketio.on('message')
def handle_message(message):
    print('Received message:' + message)
    if message != "User connected!":
        send(message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app,host="localhost")

# def get_anime(id):
#     url = f"https://api.jikan.moe/v4/anime/{id}/full/"
#     response = r.get(url)
#     if response.ok:
#         data = response.json()
        
#         output = {
#             'anime_name': data['title'],
#             'anime_name_english': data['title_english'],
#             'genres': [obj['name']for obj in data['genres']],
#             'anime_type': data['species']['name'],
#             'episodes': data['episodes'],
#             'image_url': data['images']['jpg']['image_url'],
#             'synopsis': data['synopsis'],
#             'producers': [co['name'] for co in data['producers']],
#             }
#         return output 
    


@app.route("/", methods=["GET","POST"])
def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            
            user = User.query.filter_by(username=username).first()
            if not user:
                return render_template("login.html", form=form)
            else:       
                if user.check_password(password):
                    login_user(user)
                    return redirect(url_for('index_page'))
                else:
                    return render_template("login.html", form=form)
        else:
            return render_template("login.html", form=form)
    else:
        return render_template("login.html", form=form) 


@app.route("/register", methods=["GET","POST"])
def register_page():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            new_user = User(first_name, last_name, username=username,email=email, password=password)
            new_user.save()
            
            return redirect(url_for('login_page'))

        else:
            return render_template("register.html", form=form)
    else:
        return render_template("register.html", form=form)

    
@app.route("/index", methods=["GET"])
@login_required
def index_page():

    return render_template('index.html')
        
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login_page"))

# @app.route("/search", methods=["GET", "POST"])
# #@login_required
# def search_page():
#     form = SearchForm()
#     if request.method == 'POST':
#         if form.validate():
#             animesearch = form.animesearch.data
#             data = get_anime(animesearch)
#             return render_template('search.html', form = form, data = data)
#     return render_template('search.html', form = form)

@app.route("/like",methods=["POST"])
def like_anime():
    data = request.json
    print(data)
    return {"hi":"world"}

@app.route("/message", methods=["GET", "POST"])
@login_required
def message_page():
    return render_template("messages.html")