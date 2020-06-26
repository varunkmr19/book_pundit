import requests
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from bookpundit import app, db, bcrypt
from bookpundit.forms import RegistrationForm, LoginForm, BookSearchForm, ReviewForm
from bookpundit.models import User, Book, Review
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import or_, and_, func



@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('search'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('index.html', form=form, title='Home Page')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = BookSearchForm()
    if form.validate_on_submit():
        search = "%" + form.search_query.data + "%"
        result = Book.query.filter( or_(Book.isbn.like(search), Book.title.like(search), Book.author.like(search), Book.year.like(search)) ).all()
        
        if result:
            return render_template('search.html', form=form, results=result)
        else:
            return render_template('search.html', form=form, message='No result found please try again!')
    
    return render_template('search.html', form=form)



@app.route("/<string:isbn>", methods=['GET', 'POST'])
@login_required
def book(isbn):
    API_KEY = 'oI66dRPDwn4Pr2FtS5LGRw'

    book_data = Book.query.filter_by(isbn=isbn).first()
    
    # API call to fetch rating from goodreads.com
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":API_KEY, "isbns":isbn}).json()
    goodreads_avg = res['books'][0]['average_rating']
    goodreads_count = res['books'][0]['ratings_count']
    

    rating_list = Review.query.filter_by(book_id=book_data.id).all()
    avg_rating = None

    # calculates avg rating from my database
    if rating_list is not None:
        total_reviews = int(Review.query.filter_by(book_id=book_data.id).count())
        avg_rating = 0
        if total_reviews > 0:
            for item in rating_list:
                avg_rating += int(item.rating)
            avg_rating /= total_reviews
            avg_rating = round(float(avg_rating), 2)

    # get reviews
    reviews = Review.query.filter_by(book_id=book_data.id).all()
    
    # handle new review post
    form = ReviewForm()
    if form.validate_on_submit():
        # check duplicate review from the same user
        review = Review.query.filter( and_(Review.username==current_user.username, Review.book_id==book_data.id) ).first()
        
        if review is not None:
            flash("You have alreday submitted a review for this book. Please review other books.", 'danger')
        else:
            review = Review(username=current_user.username, book_id=book_data.id, rating=form.rating.data, content=form.content.data)
            db.session.add(review)
            db.session.commit()
            flash("You review is successfully posted. Refresh the page to see the changes", 'success')
            

    return render_template("book.html", form=form, reviews=reviews, title=book_data.title, isbn=book_data.isbn, author=book_data.author, year=book_data.year, rating=avg_rating, goodreads_avg=goodreads_avg, goodreads_count=goodreads_count)



@app.route("/api/<string:isbn>")
def api(isbn):
    book_data = Book.query.filter_by(isbn=isbn).first()
    if book_data is None:
        abort(404)
    title = book_data.title
    author = book_data.author
    year = book_data.year
    isbn = isbn
    review_count = int(Review.query.filter_by(book_id=book_data.id).count())
    rating_list = Review.query.filter_by(book_id=book_data.id).all()
    avg_score = 0
    if review_count > 0:
        for item in rating_list:
            avg_score += int(item.rating)
        avg_score /= review_count
        avg_score = round(float(avg_score), 2)

    dic = { "title": title, "author": author, "year": year, "isbn": isbn, "review_count": review_count, "average_score": avg_score }
    print(dic)
    return jsonify(dic)