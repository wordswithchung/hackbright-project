"""Movie Ratings."""

from datetime import datetime
from flask import (Flask, jsonify, render_template, redirect, request, flash, 
                   session)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from model import Airport, Airfare, connect_to_db, db
from sqlalchemy import func


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "randomKeyGenerated1837492RandomKeyGeneratedLadidadidah00!!"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    
    return render_template("homepage.html")


# @app.route('/users')
# def user_list():
#     """Show entire list of users."""

#     users = User.query.all()

#     return render_template("user_list.html", users=users)


# @app.route('/users/<user_id>')
# def user_info(user_id):
#     """Specific user info (age, zipcode, list of movies rated and scores)."""

#     user = User.query.filter_by(user_id=user_id).first()
#     age = user.age
#     zipcode = user.zipcode
#     ratings = user.ratings

#     return render_template("user_details.html", age=age,
#                                                 zipcode=zipcode,
#                                                 ratings=ratings,
#                                                 user_id=user_id)


@app.route('/register', methods=["GET"])
def register_form():
    """Display user registration form."""

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Process registration form."""

    username = request.form.get("username")
    password = request.form.get("password")

    email_search = User.query.filter_by(email=username).all()

    if email_search == []: # not in database
        user = User(email=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")
        return redirect("/")
    else:
        flash("Email already exists. Try again.")
        return redirect("/register")


@app.route('/login')
def login_form():
    """Login form."""

    return render_template("login.html")


@app.route('/login', methods=["POST"])
def login_process():
    """Verify login credentials."""

    username = request.form.get("username")
    password = request.form.get("password")

    verify_user = User.query.filter_by(email=username, password=password).all()

    if verify_user == []: # email/password combo is not in database
        flash("The email / password combo provided doesn't match our records.")
        return redirect("/register")
    else:
        user = User.query.filter_by(email=username).first()
        session["login"] = user.user_id
        flash("Logged in!")
        return redirect("/")


@app.route('/logout')
def logout():
    """Logout user."""

    del session["login"]
    flash("You have been logged out.")
    return redirect("/")

# Later...if login in session, display this button
# If login is empty list, might give an error
# Deleting makes it cleaner


@app.route('/movies')
def movie_list():
    """Show entire list of movies."""

    movies = Movie.query.order_by(Movie.title).all()

    return render_template("movie_list.html", movies=movies)


@app.route('/movies/<movie_id>')
def movie_info(movie_id):
    """Specific details about movie."""

    movie = Movie.query.filter_by(movie_id=movie_id).first()
    title = movie.title
    released_at = movie.released_at.strftime('%B %d, %Y')
    imdb_url = movie.imdb_url
    ratings = movie.ratings

    user_id = 0
    user_score = 0
    update_rating = False
    rating = False

    if session.get("login"):
        rating_exists = Rating.query.filter_by(user_id=session['login'], 
                                               movie_id=movie_id).first()
        user_id = session['login']
        if rating_exists: # yep, they rated the movie
            user_score = rating_exists.score
            update_rating = True # give option to update
        else: # they didn't rate movie; give option to rate
            rating = True 
    # pass a variable to jinja that says, "yeah, let them rate"

    # get average rating of movie

    rating_scores = [r.score for r in ratings]
    avg_rating = float(sum(rating_scores)) / len(rating_scores)

    prediction = None

    # prediction code: only predict if user hasn't rated it

    if (user_score == 0) and (user_id != 0):
        user = User.query.get(user_id)
        if user:
            prediction = user.predict_rating(movie)

    # Either use the prediction or their real rating
    if prediction:
        # User hasn't scored; use our prediction if we made one
        effective_rating = prediction

    elif user_score:
        # User has already scored; use that
        effective_rating = user_score

    else:
        # User hasn't scored, and we couldn't get a prediction
        effective_rating = None

    # Get the eye's rating, either by predicting or using real rating

    the_eye = (User.query.filter_by(email="eye").one())
    eye_rating = Rating.query.filter_by(
        user_id=the_eye.user_id, movie_id=movie_id).first()

    if eye_rating is None:
        eye_rating = the_eye.predict_rating(movie)

    else:
        eye_rating = eye_rating.score

    if eye_rating and effective_rating:
        difference = abs(eye_rating - effective_rating)

    else:
        # We couldn't get an eye rating, so we'll skip difference
        difference = None

    BERATEMENT_MESSAGES = [
        "I suppose you don't have such bad taste after all.",
        "I regret every decision that I've ever made that has " +
            "brought me to listen to your opinion.",
        "Words fail me, as your taste in movies has clearly " +
            "failed you.",
        "That movie is great. For a clown to watch. Idiot.",
        "Words cannot express the awfulness of your taste."
    ]

    if difference is not None:
        beratement = BERATEMENT_MESSAGES[int(difference)]

    else:
        beratement = None   


    return render_template("movie_details.html", title=title,
                                                 released_at=released_at,
                                                 imdb_url=imdb_url,
                                                 ratings=ratings,
                                                 movie_id=movie_id,
                                                 user_score=user_score,
                                                 update_rating=update_rating,
                                                 rating=rating,
                                                 user_id=user_id,
                                                 prediction=prediction,
                                                 average=avg_rating,
                                                 beratement=beratement)


@app.route('/rate_movie', methods=["POST"])
def rate_movie():
    """Display movie rating form."""

    # updates the database with new movie rating for user

    update_rating = request.form.get("update_rating")
    rating = request.form.get("rating") 
    user_id = request.form.get("user_id")
    movie_id = request.form.get("movie_id")

    if update_rating:
        current_rating = Rating.query.filter_by(movie_id=movie_id, 
                                        user_id=user_id).first()
        current_rating.score = update_rating
        db.session.commit()
        score = update_rating

    if rating:
        rate = Rating(movie_id=movie_id, user_id=user_id, score=rating)
        db.session.add(rate)
        db.session.commit()
        score = rating

    return jsonify(score)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)
