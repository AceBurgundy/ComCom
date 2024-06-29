import re
from typing import List, Optional
from wtforms.validators import DataRequired, Length, ValidationError, Email
from wtforms import StringField, PasswordField, EmailField
from Engine.helpers import CheckProfanity
from flask_wtf import FlaskForm
from Engine.models import User

def validate_username(form, field) -> None:
    """
    Validates username

    Raises validation error:
        If username is empty or taken
    """
    if not field.data:
        raise ValidationError("Username cannot be empty")

    user: Optional[User] = User.query.filter_by(username=field.data).first()

    if user:
        raise ValidationError("Username already taken")

def validate_email(form, field) -> None:
    """
    Validates email

    Raises validation error:
        If email is empty or taken
    """
    if not field.data:
        raise ValidationError("Email cannot be empty")

    user: Optional[User] = User.query.filter_by(email=field.data).first()

    if user:
        raise ValidationError("Email already taken")

def validate_password(form, field) -> None:
    """
    Validates password

    Raises validation error:
        If password is empty
        If password contains restricted words
        If password contains restricted characters
        If password does not contain atleast 1 number
        If password does not contain atleast 1 symbol
    """
    if not field.data:
        raise ValidationError("Password cannot be empty")

    # Perform additional password validation logic here
    password = field.data

    # Check for restricted words
    restricted_words = ["where","select","update","delete",".schema","from","drop"]

    for word in restricted_words:
        if word.lower() in password.lower():
            raise ValidationError("Password contains a restricted word")

    # Check for restricted characters
    restricted_characters: List[str] = ["!", "#", "$"]

    for char in restricted_characters:
        if char in password:
            raise ValidationError("Password contains a restricted character")

    # Check for at least one number and one symbol
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number")

    if not re.search(r"[!@#$%^&*()_+}{\":?></*+[;'./,]", password):
        raise ValidationError("Password must contain at least one symbol")

class RegisterForm(FlaskForm):
    """
    Flaskform for registering user
    """
    register_username: StringField = StringField(u'Username', id="username", validators=[
        DataRequired(message="Add a username"),
        Length(min=2, max=50),
        validate_username,
        CheckProfanity()
    ])

    register_email: StringField = StringField(u'Email', id="register-email", validators=[
        DataRequired(message="Should be a working email"),
        Email(),
        Length(min=2, max=120),
        validate_email,
    ])

    register_password: PasswordField = PasswordField(u'Password', id="regpassword", validators=[
        DataRequired("Please add a password"),
        Length(min=2, max=40),
        CheckProfanity(),
        validate_password
    ])

class LoginForm(FlaskForm):

    login_email: EmailField = EmailField(u'Email', id="login-email", validators=[
        DataRequired(message="Should be a working email"),
        Length(min=2,max=120),
        Email(),
    ])

    def validate_login_email(self, login_email) -> None:
        """
        Validates login email

        Raises validation error:
            If email is empty or not found
        """
        if not login_email.data:
            raise ValidationError("Email cannot be empty")

        user: Optional[User] = User.query.filter_by(email=login_email.data).first()

        if not user:
            raise ValidationError("\nEmail not found or User not yet registered")

    login_password: PasswordField = PasswordField(u'Password', id="logpassword", validators=[
        DataRequired("Please add a password"),
        Length(min=2, max=40),
        CheckProfanity()
    ])

    def validate_login_password(self, login_password) -> None:
        """
        Validates password

        Raises validation error:
            If password is empty
        """
        if not login_password.data:
            raise ValidationError("Password cannot be empty")