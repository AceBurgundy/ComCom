from flask_login import UserMixin # type: ignore
from typing import Optional, Dict, Any
from Engine import db, login_manager
from datetime import datetime
from enum import Enum
import json

@login_manager.user_loader
def load_user(user_id) -> Optional['User']:
    """
    retrieves a user by its ID or None
    """
    id: int = int(user_id)
    return User.query.get(id)

def prettify(dictionary_data: Dict[str, Any], table_name: str) -> str:
    """
    The function `prettify` takes a dictionary and a table name as input, and prints a prettified
    representation of the dictionary data along with the table name.

    Args:
    -----
      dictionary_data (Dict[str, any]): A dictionary containing the data of a model object.
      table_name (str): A string representing the name of the table or model object.
    """
    fields: str = json.dumps(dictionary_data, indent=4)
    return f"{table_name}\n{fields}"

class BaseModel(db.Model): # type: ignore

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.now, nullable=False)
    date_updated = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    date_removed = db.Column(db.DateTime())

class User(BaseModel, UserMixin):

    __tablename__ = 'user'

    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(100), nullable=False, default='user.webp')
    password = db.Column(db.String(200), nullable=False)
    last_online = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)
    night_mode = db.Column(db.Boolean(), nullable=False, default=True)

    rooms = db.relationship('UserRoom', back_populates='user')

    sent_notifications = db.relationship('Notification', foreign_keys='Notification.sender_id', backref='sender', lazy=True, cascade="all, delete-orphan")
    received_notifications = db.relationship('Notification', foreign_keys='Notification.receiver_id', backref='receiver', lazy=True, cascade="all, delete-orphan")

    """
    >>> files = db.relationship('File', backref='user', lazy=True, passive_deletes=True)

    If files will be used, it will have a conflict with File.uploader

    Suggestions:
        - Adding the parameter overlaps="files,user" to the backref or relationship definitions in both classes. This parameter helps SQLAlchemy disambiguate the relationships and resolve the conflict.
        - Alternatively, you can consider using viewonly=True for one or more relationships if they are meant to be read-only.
    """

    # def __repr__(self) -> str:
    #     """
    #     Presents a visual representation of the object
    #     """
    #     return prettify(self.__dict__, self.__tablename__)

class Notification(BaseModel):

    __tablename__ = 'notification'

    class ALLOWED_TYPES(Enum):
        STANDARD = 'standard'
        JOIN = 'join'
        CONFIRM = 'confirm'
        WARN = 'warn'
        ERROR = 'error'

    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)

    def __init__(self, message: str, type: ALLOWED_TYPES, sender: Any, receiver: Any, room: Any) -> None:
        self.message = message
        self.type = type.value
        self.sender_id = sender.id
        self.receiver_id = receiver.id
        self.room_id = room.id

    def __repr__(self) -> str:
        """
        Presents a visual representation of the object
        """
        return f"Notification(message={self.message}, sender_id={self.sender_id}, receiver_id={self.receiver_id}, room_id={self.room_id}, type={self.type})"

class Room(BaseModel):

    __tablename__ = "room"

    code = db.Column(db.String(9), nullable=False)
    title = db.Column(db.String(100), nullable=False, default="New Room")
    description = db.Column(db.String(200))

    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    admin = db.relationship('User', uselist=False)

    members = db.relationship('UserRoom', back_populates='room')
    notifications = db.relationship('Notification', backref='room', lazy=True, cascade="all, delete-orphan")

    announcements = db.relationship('RoomAnnouncement', backref='room', lazy=True, passive_deletes=True)
    files = db.relationship('File', backref='room', lazy=True, cascade="all, delete-orphan")

    def __init__(self, code: str, title: str, description: str, admin: User) -> None:
        """
        A new constructor that provides data to the attributes initially.
        """
        self.code = code
        self.title = title
        self.description = description
        self.admin = admin

        new_member: UserRoom = UserRoom(user=admin, room=self)
        db.session.add(new_member)
        db.session.commit()

    def __repr__(self) -> str:
        """
        Presents a visual representation of the object
        """
        return prettify(self.__dict__, self.__tablename__)

class RoomAnnouncement(BaseModel, UserMixin):

    __tablename__ = 'room_announcement'

    text = db.Column(db.Text)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, text, room_id) -> None:
        """
        A new constructor that provides data to the attributes initially.
        """
        self.text = text
        self.room_id = room_id

    def __repr__(self) -> str:
        """
        Presents a visual representation of the object
        """
        return prettify(self.__dict__, self.__tablename__)

class UserRoom(BaseModel):

    __tablename__ = "user_room"

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', back_populates='rooms')
    room = db.relationship('Room', back_populates='members')

    def __init__(self, user: User, room: Room) -> None:
        """
        Initializes the UserRoom instance with a user and a room.
        """
        self.user = user
        self.room = room

class File(BaseModel):

    __tablename__ = "file"

    file_name = db.Column(db.String(200), nullable=False)
    file_format = db.Column(db.String(5), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id', ondelete='CASCADE'), nullable=False)

    uploader = db.relationship('User', backref='uploaded_files')

    def __repr__(self) -> str:
        """
        Presents a visual representation of the object
        """
        return prettify(self.__dict__, self.__tablename__)
