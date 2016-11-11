


// http://stackoverflow.com/a/33319433

function showResults(results) {



    $('#display-search-results').html(results);
}

function submitForm(evt) {

    evt.preventDefault();

    var formData = {
        'depart'    : $('#input-from').val(),
        'month'     : $('#input-month').val(),
        'duration'  : $('#input-duration').val()
    };

    $.post('/search.json', formData, showResults);
};

$('#form-submission').on('submit', submitForm);







// $("#form-country_v1").typeahead('val',"test");
// http://stackoverflow.com/questions/17278709/set-selected-value-of-typeahead

// code from ratings //////////////////////////////////
// function showRating(rating){
//   $('#user-score').html("Your User Score: " + rating);
// }

// function updateRating(evt){
//   evt.preventDefault();

//   var formInputs = {
//     'update_rating': $("input:radio[name=update_rating]:checked").val(),
//     'user_id': $("#update-user").val(),
//     'movie_id': $("#update-movie").val()
//   };

// $.post("/rate_movie", formInputs, showRating);
// }

// $('#update-rating-form').on('submit', updateRating);

function showNewRating(rating) {
  $('#new-user-score').html("Your User Score: " + rating);
}

function newRating(evt) {
  evt.preventDefault();

  var formInputs = {
    'rating': $("input:radio[name=rating]:checked").val(),
    'user_id': $("#new-user").val(),
    'movie_id': $("#new-movie").val()
  };

  $.post("/rate_movie", formInputs, showNewRating);
}

$('#new-rating-form').on('submit', newRating);

@app.route('/rate_movie', methods=["POST"])
def rate_movie():
    """Display movie rating form."""

    // # updates the database with new movie rating for user

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
