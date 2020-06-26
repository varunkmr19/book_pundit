from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from bookpundit.models import User

class BookSearchForm(FlaskForm):
    search_query = StringField('Search by ISBN, title, author or year', validators=[DataRequired()])
    submit = SubmitField('Search')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[NumberRange(min=1, max=5, message='Invalid length')])
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post')