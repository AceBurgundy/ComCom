from wtforms import StringField, SubmitField, TextAreaField, PasswordField # type: ignore
from wtforms.validators import DataRequired, Length, ValidationError # type: ignore
from flask_wtf.file import FileField, FileAllowed # type: ignore
from Engine.helpers import CheckProfanity
from flask_wtf import FlaskForm # type: ignore
from Engine.models import User

class ProfileForm(FlaskForm):
    """
    Flask form for editing user profile.
    """
    submit: SubmitField = SubmitField('Update')

    banner: TextAreaField = TextAreaField(id="motto", validators=[DataRequired(),Length(min=20, max=200), CheckProfanity()])

    profile_picture: FileField = FileField(id='profile-picture-input', validators=[FileAllowed(['jpeg', 'png', 'jpg', 'webp'])])

    username: StringField = StringField(id='username', validators=[DataRequired(), Length(max=50), CheckProfanity()])

    def validate_username(self, username) -> None:
        """
        Returns None but raises ValidationError is user was not found.
        """
        if User.query.filter_by(username=username.data) == True:
            raise ValidationError("Username already taken")

class DeleteAccountForm(FlaskForm):
    """
    Flask form for deleting user.
    """
    submit: SubmitField = SubmitField('Delete', id="delete-account-proceed")

    password: PasswordField = PasswordField(id='delete-account-password-input', validators=[DataRequired()])
