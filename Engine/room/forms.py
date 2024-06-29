from wtforms import StringField, TextAreaField, ValidationError # type: ignore
from wtforms.validators import DataRequired, Length # type: ignore
from Engine.helpers import CheckProfanity # type: ignore
from flask_wtf import FlaskForm # type: ignore
from typing import Optional

from Engine.models import Room # type: ignore

class CreateRoomForm(FlaskForm):
    """
    Flask form for creating rooms
    """
    title: StringField = StringField('Title', id="create-room__title", validators=[DataRequired(message="Title Needed"), Length(max=100), CheckProfanity(message="not accepted")])
    body: TextAreaField = TextAreaField('Body', id="create-room__body", validators=[DataRequired(message="Content Required"), Length(max=3000), CheckProfanity(message="not accepted")])

class JoinRoomForm(FlaskForm):

    code: StringField = StringField('Room Code', id="room-options-join-input", validators=[DataRequired(message="Enter room code"), Length(max=11), CheckProfanity(message="not accepted")])

    def validate_code(self, code) -> None:
        """
        Raises ValidationError if room not found
        """
        room: Optional[Room] = Room.query.filter_by(code=code.data).first()

        if room is None:
            raise ValidationError("Room not found")