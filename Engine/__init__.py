from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # type: ignore
from flask_socketio import SocketIO # type: ignore
from flask import Flask

login_manager: LoginManager = LoginManager()
login_manager.login_view = 'user.login' # type: ignore

db: SQLAlchemy = SQLAlchemy()
socket_io: SocketIO = SocketIO()

def create_app() -> Flask:
    """
    Creates and configures an instance of the Flask application.

    This function initializes the Flask application, sets up the configuration,
    initializes the database and socketio, and registers the blueprints for the
    index, candidate, and error views.

    Returns:
    --------
        app: A Flask application instance.
    """

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "dsfgkuhadgsfkuhjgasdejfkhdxfgiuksadhgfui"
    app.config['SESSION_TYPE'] = "filesystem"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    login_manager.init_app(app)
    db.init_app(app)
    socket_io.init_app(app)

    from Engine.user.views import user
    from Engine.room.views import room
    from Engine.index.views import index
    from Engine.profile.views import profile
    from Engine.errors.handlers import errors

    app.register_blueprint(user)
    app.register_blueprint(room)
    app.register_blueprint(index)
    app.register_blueprint(errors)
    app.register_blueprint(profile)

    return app
