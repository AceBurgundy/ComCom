from flask import Blueprint, Response as FlaskResponse, jsonify, redirect, render_template, request, session, url_for
from Engine.models import Notification, Room, RoomAnnouncement, User, UserRoom
from flask_login import current_user, login_required # type: ignore
from werkzeug.wrappers.response import Response as WerkzeugResponse
from flask_socketio import emit, join_room, leave_room, send # type: ignore
from Engine.room.forms import CreateRoomForm, JoinRoomForm
from typing import Any, Callable, Dict, List, Optional
from Engine import db, socket_io
from random import choice
import string
import json

room: Blueprint = Blueprint("room", __name__, template_folder="templates/room", static_folder="static/room")

def get_room(room_code: str) -> Optional[Room]:
    """
    Returns a specific room and its data
    """
    return Room.query.filter_by(code=room_code).first()

def get_user_rooms() -> List[Dict[str, str]]:
    """
    Returns the users room.

    This is used for displaying all rooms the user have on the left side of their screen
    """
    return [{
        "code": user_room.room.code,
        "title": user_room.room.title,
        "description": user_room.room.description
    } for user_room in current_user.rooms] if len(current_user.rooms) > 0 else []

@room.get("/room/<room_code>/open")
@login_required
def open_room(room_code: str) -> FlaskResponse|str:
    """
    Opens a specific room with the users rooms.

    Returns:
    --------
        renders room.html template with the room data
    """
    create_room_form: CreateRoomForm = CreateRoomForm()

    page_title: str = "DASHBOARD"
    image_file: str = url_for(
        'static',
        filename='profile_pictures/' + current_user.profile_picture
    )

    matched_room: Optional[Room] = get_room(room_code)

    if matched_room is None:
        return jsonify({
            "status": "error",
            "message": ["Room not found"]
        })

    return render_template(
        "room.html",
        create_room_form=create_room_form,
        room=matched_room,
        user_rooms=get_user_rooms(),
        page_title=page_title,
        image_file=image_file
    )

@socket_io.on('join')
def on_join(data) -> None:
    """
    Joins a room using Flask-SocketIO
    """
    room_code = data['room']

    # Get the current room the user is in from the session
    current_room_code = session.get('current_room_code')

    if current_room_code:
        if current_room_code != room_code:
            leave_room(current_room_code)
            emit('left', f"{current_user.username} left the room {current_room_code}", to=current_room_code)

    join_room(room_code)
    emit('joined', f"{current_user.username} joined the room {room_code}", to=room_code)

    # Update the session to the new room
    session['current_room_code'] = room_code

@socket_io.on('new-alert')
def new_alert(data) -> None:
    """
    Adds and broadcast new messages added to a room.
    """
    message: Optional[str] = data.get('message', None)
    room_code: Optional[str] = data.get('roomCode', None)

    if message is None:

        send('Alert is missing')
        return

    room: Optional[Room] = Room.query.filter_by(code=room_code).first()

    if room is None:

        send('Room to send alert to is not found')
        return

    room_annoncement: RoomAnnouncement = RoomAnnouncement(message, room.id)
    emit('alert', message, to=room.code)

    db.session.add(room_annoncement)
    db.session.commit()

@room.get("/rooms")
@login_required
def user_rooms() -> WerkzeugResponse:
    """
    Returns to the client side all rooms the user has. To be shown on the left side of the screen
    """
    return jsonify({
        "user_rooms": get_user_rooms()
    })

@room.get("/room/<room_code>/data")
@login_required
def room_data(room_code: str) -> WerkzeugResponse:
    """
    Returns the serialized data of a room.
    To be used if only the data of the room is required

    Returns:
    --------
        jsonify: The serialized room data
    """
    matched_room: Optional[Room] = get_room(room_code)

    if matched_room is None:

        return jsonify({
            "status": "error",
            "message": ["Room not found"]
        })

    room_data: Dict[str, Any] = {

        "id": matched_room.id,
        "code": matched_room.code,
        "title": matched_room.title,
        "description": matched_room.description,

        "admin": {
            "id": matched_room.admin.id,
            "username": matched_room.admin.username,
            "email": matched_room.admin.email,
            "profile_picture": matched_room.admin.profile_picture
        } if matched_room.admin else None,

        "members": [
            {
                "id": member.user.id,
                "username": member.user.username,
                "email": member.user.email,
                "profile_picture": member.user.profile_picture
            } for member in matched_room.members # type: ignore
        ],

        "announcements": [
            {
                "id": announcement.id,
                "text": announcement.text,
                "date_created": announcement.date_created,
                "date_updated": announcement.date_updated
            } for announcement in matched_room.announcements # type: ignore
        ],

        "files": [
            {
                "id": file.id,
                "file_name": file.file_name,
                "file_format": file.file_format,
                "uploader": {
                    "id": file.uploader.id,
                    "username": file.uploader.username,
                    "email": file.uploader.email,
                    "profile_picture": file.uploader.profile_picture
                }
            } for file in matched_room.files # type: ignore
        ]

    }

    print(json.dumps(room_data, indent=4))

    return jsonify({
        "status": "success",
        "data": room_data
    })

@room.post("/room/create")
@login_required
def create_room() -> WerkzeugResponse:
    """
    Creates a new room
    """
    create_room_form: CreateRoomForm = CreateRoomForm()

    if not create_room_form.validate():
        return jsonify({
            'message': [field.errors for field in create_room_form if field.errors],
            'status': 'error'
        })

    title: Optional[str] = create_room_form.title.data
    description: Optional[str] = create_room_form.body.data

    if title is None:
        return jsonify({'message': 'Title cannot be empty', 'status': 'error'})

    if description is None:
        return jsonify({'message': 'Description cannot be empty', 'status': 'error'})

    def create_code() -> str:
        """
        Creates a 9 letter code for a new room
        """
        letter: Callable = lambda: choice(string.ascii_lowercase)
        return ''.join(letter() for _ in range(9))

    while True:
        new_code: str = create_code()
        room_exists: Optional[Room] = Room.query.filter_by(code=new_code).first()

        if room_exists is None:
            new_room: Room = Room(code=new_code, title=title, description=description, admin=current_user) # type: ignore

            db.session.add(new_room)
            db.session.commit()

            return jsonify({'link': url_for('room.open_room', room_code=new_code), 'status': 'success'})

@room.get("/room")
@login_required
def get_rooms() -> FlaskResponse:
    """
    Returns a list of rooms whom the current user is a member of.
    """
    rooms: Dict[str, Dict[str, str]] = {}

    for user_room in current_user.rooms:
        code: str = f"/room/{user_room.room.code}"

        rooms[code] = {
            "title": user_room.room.title,
            "description": user_room.room.description
        }

    return jsonify(rooms)

@room.post("/room/join")
@login_required
def room_join() -> FlaskResponse|WerkzeugResponse:
    """
    Joins a user to a room.
    """
    join_room_form: JoinRoomForm = JoinRoomForm()

    if not join_room_form.validate():
        return jsonify({
            'message': [field.errors for field in join_room_form if field.errors],
            'status': 'error'
        })

    room: Optional[Room] = Room.query.filter_by(code=join_room_form.code.data).first()

    if room is None:
        return jsonify({'message': 'Room not found', 'status': 'error'})

    a_room_member: Optional[UserRoom] = UserRoom.query.filter_by(user_id=current_user.id, room_id=room.id).first()

    if not a_room_member:

        notification = Notification(
            message=f"{current_user.username} wants to join {room.title}",
            type=Notification.ALLOWED_TYPES.JOIN,
            sender=current_user,
            receiver=room.admin,
            room=room
        )

        db.session.add(notification)
        db.session.commit()

        socket_io.emit('update_notification')
        return jsonify({"message": "Request sent", "status": "success"})

    return redirect(url_for('index._index'))

@room.post("/room/join/accept")
@login_required
def accept_join_room() -> FlaskResponse|WerkzeugResponse:
    """
    Joins a user to a room.
    """
    notification_id = request.form.get('notification_id')
    notification_room_id = request.form.get('notification_room_id')

    room: Optional[Room] = Room.query.get(notification_room_id)
    notification: Optional[Notification] = Notification.query.get(notification_id)

    if room is None:
        return jsonify({'message': 'Room not found', 'status': 'error'})

    if notification is None:
        return jsonify({'message': 'Notification not found', 'status': 'error'})

    # The one who sent the notification
    # In this case, it is the user who wants to join the group
    user: Optional[User] = User.query.get(notification.sender_id)

    if user is None:
        return jsonify({'message': 'User to join not found', 'status': 'error'})

    accepted_admin_notification = Notification(
        message=f"{user.username} has been accepted to join {room.title}",
        type=Notification.ALLOWED_TYPES.STANDARD,
        sender=room.admin,
        receiver=room.admin,
        room=room
    )

    accepted_user_notification = Notification(
        message=f"You have been accepted to {room.title}",
        type=Notification.ALLOWED_TYPES.STANDARD,
        receiver=user,
        sender=room.admin,
        room=room
    )

    # Adding the new user to the room
    new_user_room = UserRoom(user, room)

    db.session.add(new_user_room)
    db.session.add(accepted_admin_notification)
    db.session.add(accepted_user_notification)

    # Delete all request to join notifications including the duplicated ones.
    notifications_to_delete = Notification.query.filter_by(message=notification.message).all()

    for notification in notifications_to_delete:
        db.session.delete(notification)

    db.session.commit()

    socket_io.emit('update_notification')

    # refresh link must be used if the user requested to join when he's not at room.open_room html else get only the code to add the data
    return jsonify({
        "message": "Request approved",
        "status": "success",
        "redirect_link": url_for('room.open_room', room_code=room.code)
    })

@room.post("/room/<room_code>/leave")
@login_required
def leave(room_code) -> FlaskResponse|WerkzeugResponse:
    """
    Removes a user from a room
    """
    room = Room.query.filter_by(code=room_code).first()

    if not room:

        return jsonify({
            "status": "error",
            "message": "Cannot leave room. Room cannot be found"
        })

    user_room = UserRoom.query.filter_by(user=current_user, room=room).first()

    if not user_room:

        return jsonify({
            "status": "error",
            "message": "Cannot leave room. User's connection to the room cannot be found"
        })

    db.session.delete(user_room)
    db.session.commit()

    # Delete room if the user who left is the only user
    if len(room.members) <= 0:
        db.session.delete(room)

    else:
        # Set the next user if not the previous left user to be the new admin
        user_index: int = 0

        while True:

            room_member = room.members[user_index].user

            if room_member.id != current_user.id:
                room.admin = room_member
                break
            else:
                user_index += 1

    db.session.commit()
    still_has_rooms: bool = len(current_user.rooms) > 0
    return redirect(url_for('room.open_room', room_code=current_user.rooms[-1].room.code) if still_has_rooms else url_for('index._index'))

@room.post("/room/join/decline")
@login_required
def decline_join_room() -> FlaskResponse|WerkzeugResponse:
    """
    Joins a user to a room.
    """
    notification_id = request.form.get('notification_id')
    notification_room_id = request.form.get('notification_room_id')

    room: Optional[Room] = Room.query.get(notification_room_id)
    notification: Optional[Notification] = Notification.query.get(notification_id)

    if room is None:
        return jsonify({'message': 'Room not found', 'status': 'error'})

    if notification is None:
        return jsonify({'message': 'Notification not found', 'status': 'error'})

    # The one who sent the notification
    # In this case, it is the user who wants to join the group
    user: Optional[User] = User.query.get(notification.sender_id)

    if user is None:
        return jsonify({'message': 'User to join not found', 'status': 'error'})

    accepted_admin_notification: Notification = Notification(
        message=f"{user.username} has been declined from joining {room.title}",
        type=Notification.ALLOWED_TYPES.STANDARD,
        sender=room.admin,
        receiver=room.admin,
        room=room
    )

    accepted_user_notification: Notification = Notification(
        message=f"You have been declined from joining {room.title}",
        type=Notification.ALLOWED_TYPES.STANDARD,
        receiver=user,
        sender=room.admin,
        room=room
    )

    db.session.add(accepted_admin_notification)
    db.session.add(accepted_user_notification)

    # Delete all request to join notifications including the duplicated ones.
    notifications_to_delete: List[Notification] = Notification.query.filter_by(message=notification.message).all()

    for notification in notifications_to_delete:
        db.session.delete(notification)

    db.session.commit()

    socket_io.emit('update_notification')

    # refresh link must be used if the user requested to join when he's not at room.open_room html else get only the code to add the data
    return jsonify({
        "message": "Request declined. See notification",
        "status": "success",
    })
