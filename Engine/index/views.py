from flask import Response as FlaskResponse, redirect, render_template, request, session, url_for, Blueprint
from werkzeug.wrappers.response import Response as WerkzeugResponse
from flask_login import current_user, login_required # type: ignore
from Engine.room.forms import CreateRoomForm, JoinRoomForm
from Engine.models import Room, UserRoom
from typing import Dict, List
from flask import jsonify
from flask import request
from Engine import db

index: Blueprint = Blueprint('index', __name__, template_folder='templates/index', static_folder='static/index')

@index.get("/night-mode")
def get_current_mode() -> FlaskResponse:
    """
    Retrieve the current night mode setting for the user.

    Returns:
        JSON: The current night mode setting.
    """
    return jsonify({
        "mode": current_user.night_mode
    })

@index.post("/night-mode")
def set_current_mode() -> FlaskResponse:
    """
    Set the current night mode setting for the user.

    Returns:
    --------
        Response: JSON response indicating the success status of the operation.
            - 'status' (bool): Indicates whether the operation was successful or not.
    """
    data = request.get_json()
    mode = data.get('mode')

    if mode not in ['Day', 'Night']:

        return jsonify({
            "status": "error",
            "message": "Error in setting mode"
        })

    current_user.night_mode = False if mode == 'Day' else True
    db.session.commit()

    return jsonify({
        "status": True
    })

@index.get("/")
@login_required
def _index() -> str | WerkzeugResponse:
    """
    Load the root page.

    Returns:
    --------
        Renders index.html template with its necessary data.
    """
    page_title: str = "DASHBOARD"
    image_file: str = url_for(
        'static',
        filename='profile_pictures/' + current_user.profile_picture
    )

    create_room_form: CreateRoomForm = CreateRoomForm()
    join_room_form: JoinRoomForm = JoinRoomForm()
    rooms: List[Room] = current_user.rooms

    if len(rooms) > 0:
        latest_user_room: UserRoom = current_user.rooms[len(current_user.rooms) - 1]
        return redirect(url_for('room.open_room', room_code=latest_user_room.room.code))

    return render_template(
        "index.html",
        image_file=image_file,
        page_title=page_title,
        rooms=rooms,
        room_count=len(rooms),
        create_room_form=create_room_form,
        join_room_form=join_room_form
    )

@index.get("/is_logged_in")
def is_logged_in():
    """
    Returns if there is a current_user (logged_in) or not

    This does this by checking if
        current_user.__class__.__name__ != 'AnonymousUserMixin'

    a logged in user doesn't use 'AnonymousUserMixin' but rather the database model used for saving User
    """
    return jsonify({
        "status": "success",
        "logged_in": current_user.__class__.__name__ != 'AnonymousUserMixin'
    })

@index.get("/notifications")
def notifications() -> FlaskResponse:
    """
    Returns the current users notifications
    """
    received_notifications_query = current_user.received_notifications[-5:] if len(current_user.received_notifications) > 5 else current_user.received_notifications

    notifications: List[Dict[str, str]] = []

    for notification in received_notifications_query:

        notifications.append({
            "id": notification.id,
            "message": notification.message,
            "type": notification.type,
            "roomId": notification.room_id
        })

    return jsonify(notifications)

@index.get("/about")
@login_required
def about() -> str:
    """
    Loads the about page.

    Returns:
        Renders about.html template with its necessary data.
    """
    page_title: str = "DASHBOARD"
    image_file: str = url_for(
        'static',
        filename='profile_pictures/' + current_user.profile_picture
    )

    return render_template(
        "about.html",
        image_file=image_file,
        page_title=page_title
    )

