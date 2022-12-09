# This module contains the templates for all forms utilised in the app.

from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import BooleanField, PasswordField, RadioField
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class SignupForm(FlaskForm):
    """
    A template for a simple registration form. Fields in the form include:
    - Email -> `str`
    - Username -> `str`
    - Password -> `str`
    - Confirm Password -> `str`
    - Age Group -> radiobutton
    - reCAPTCHA -> type depending on config used
    - Submit -> button

    Created using :class:`flask_wtf.FlaskForm` as a base. More information
    about :class:`flask_wtf.FlaskForm` can be found in the Flask-WTF docs:
    https://flask-wtf.readthedocs.io/en/latest/
    """

    # A string field for entering the email address
    email = StringField('Email', validators=[DataRequired(), Email()])

    # A string field for entering the username
    name = StringField('Username', validators=[DataRequired()])

    # A password field for entering the password
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('confirm', message='Passwords must match')
        ]
    )
    confirm = PasswordField('Confirm Password')

    # A radio field for choosing age group
    age_group = RadioField('Age Group', choices=[(0, '5 to 17 years'),
                                                 (1, '18 to 64 years'),
                                                 (2, '65 years and older')],
                            validators=[DataRequired()], default=2)

    # reCAPTCHA to ensure form isn't spammed
    recaptcha = RecaptchaField()

    # Submit button
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """
    A template for a simple Sign Up form. Fields in the form include:
    - Email -> `str`
    - Password -> `str`
    - Remember -> `bool`
    - Submit -> button

    Created using :class:`flask_wtf.FlaskForm` as a base. More information
    about :class:`flask_wtf.FlaskForm` can be found in the Flask-WTF docs:
    https://flask-wtf.readthedocs.io/en/latest/
    """

    # A string field for entering the email
    email = StringField('Email', validators=[DataRequired(), Email()])

    # A password field for entering the password
    password = PasswordField('Password', validators=[DataRequired()])

    # A RememberMe field
    remember = BooleanField('Remember Me')

    # Submit button
    submit = SubmitField('Login')
