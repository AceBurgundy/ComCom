from flask import Blueprint, Response, jsonify, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user # type: ignore
from Engine.user.forms import RegisterForm, LoginForm
from Engine.models import User
from sqlalchemy import insert
from typing import Optional
from Engine import db

# Create a blueprint for user routes
user: Blueprint = Blueprint('user', __name__, template_folder='templates/user', static_folder='static/user')

@user.get("/login")
def login_form() -> str:
    """
    Displays login form.

    Returns:
    --------
        renders login.html template with the login form
    """
    logout_user()
    return render_template("login.html", form=LoginForm())

@user.post("/login")
def login() -> Response:
    """
    Logs user in.

    Returns:
    --------
        Response: JSON response indicating login status and optional message.
            - 'status' (str): Indicates the status of the login attempt ('success' or 'error').
            - 'message' (list of str): Additional information about the login attempt, such as error messages.
    """
    form: LoginForm = LoginForm(request.form)

    email_input: Optional[str] = form.login_email.data

    if not email_input:

        return jsonify({
            'status': 'error',
            'message': ["Email cannot be empty"]
        })

    password_input: Optional[str] = form.login_password.data

    if not password_input:

        return jsonify({
            'status': 'error',
            'message': ["Password cannot be empty"]
        })

    user: Optional[User] = User.query.filter_by(email=email_input.strip()).first()

    if not form.validate():

        return jsonify({
            'status': 'error',
            'message': [field.errors for field in form if field.errors]
        })

    if user and check_password_hash(user.password, password_input):

        login_user(user)
        return jsonify({
                'status': 'success',
                'url': url_for('index._index')
        })

    else:

        return jsonify({
                'status': 'error',
                'message': ["No matching password"]
        })

@user.get("/logout")
def logout():
    """
    Logs user out.

    Returns:
        Redirects to the login_form route
    """
    logout_user()
    return redirect(url_for('user.login_form'))


@user.get("/register")
def register_form() -> str:
    """
    Displays registration form.

    Returns:
    --------
        renders register.html template with the registration form
    """
    return render_template("register.html", form=RegisterForm())

@user.post("/register")
def register() -> Response:
    """
    Registers user.

    Returns:
    --------
        Response: JSON response indicating register status and optional message.
            - 'status' (str): Indicates the status of the register attempt ('success' or 'error').
            - 'message' (list of str): Additional information about the register attempt, such as error messages.
    """
    form: RegisterForm = RegisterForm(request.form)

    if not form.validate():

        return jsonify({
            'status': 'error',
            'message': [field.errors for field in form if field.errors]
        })

    username_input: Optional[str] = form.register_username.data
    email_input: Optional[str] = form.register_email.data
    password_input: Optional[str] = form.register_password.data

    if not password_input:

        return jsonify({
            'status': 'error',
            'message': ["Password cannot be empty"]
        })

    encrypted_password: str = generate_password_hash(password_input)

    try:
        db.session.execute(
            insert(User).values(
                username=username_input,
                email=email_input,
                password=encrypted_password
            )
        )

        db.session.commit()

        return jsonify({
            'status': 'success',
            'url': url_for('user.login_form')
        })
    except:
        return jsonify({
            'status': 'error',
            'message': ["Error in registering user"]
        })
