from typing import Optional
from flask import Blueprint, Response, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from Engine.profile.forms import DeleteAccountForm, ProfileForm
from werkzeug.wrappers import Response as RedirectResponse
from flask_login import current_user, login_required # type: ignore
from Engine.helpers import save_picture
from Engine.models import User
from Engine import db

profile: Blueprint = Blueprint('profile', __name__, template_folder='templates/profile', static_folder='static/profile')

@profile.get("/profile/<int:user_id>")
@login_required
def get_profile(user_id) -> str|RedirectResponse:
    """
    Route to retrieve and render the profile page for a user.

    Arguments:
    ----------
        user_id (int): The ID of the user to display the profile for.

    Returns:
    --------
        renders profile.html template with its forms.
    """
    user: Optional[User] = User.query.get(user_id)

    if user is None:
        return redirect(url_for('user.login'))

    user_image: str = url_for('static', filename='profile_pictures/' + user.profile_picture)
    form: ProfileForm = ProfileForm()
    delete_account_form: DeleteAccountForm = DeleteAccountForm()

    image_file: str = url_for('static', filename='profile_pictures/' + current_user.profile_picture)

    form.username.data = user.username

    return render_template(
        "profile.html",
        form=form,
        delete_account_form=delete_account_form,
        image_file=image_file,
        user_id=user_id,
        user_image=user_image
    )

@profile.post("/profile")
@login_required
def post_profile() -> str|RedirectResponse:
    """
    Route to handle updating the user's profile.

    Returns:
        response (str): Redirects to the user's profile page if the profile is successfully updated.
                        Otherwise, renders the profile page with the appropriate error messages.
    """

    form: ProfileForm = ProfileForm()
    delete_account_form: DeleteAccountForm = DeleteAccountForm()
    image_file: str = url_for('static', filename='profile_pictures/' + current_user.profile_picture)

    if not form.validate_on_submit():

        return render_template(
            'profile.html',
            form=form,
            delete_account_form=delete_account_form,
            image_file=image_file,
            error=form.errors
        )

    if form.profile_picture.data:
        current_user.profile_picture = save_picture("static/profile_pictures", form.profile_picture.data)

    current_user.username = form.username.data
    flash('Successfully updated profile')
    db.session.commit()

    return redirect(
        url_for('profile.get_profile', user_id=current_user.id)
    )

@profile.post("/change-password")
@login_required
def change_password() -> Response:
    """
    Route to handle changing the user's password.

    Returns:
        response (str): JSON response indicating the success or failure of the password change.
    """
    data = request.get_json()

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not new_password or not old_password:
        return jsonify({'status': 'success', 'message': 'Fields cannot be empty'})

    if not check_password_hash(current_user.password, old_password):
        return jsonify({'status': 'error', 'message': 'Passwords do not match'})

    current_user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Password Changed'})

@profile.post("/profile/delete")
@login_required
def delete_account() -> Response:
    """
    Route to handle deleting the user's account.

    Returns:
        response (str): JSON response indicating the success or failure of the account deletion.
    """
    delete_account_form: DeleteAccountForm = DeleteAccountForm()

    if not delete_account_form.validate_on_submit():
        return jsonify({'status': 'error', 'message': 'Fill the form properly to avoid errors'})

    input_password: Optional[str] = delete_account_form.password.data

    if not input_password:
        return jsonify({'status': 'error', 'message': 'Password is missing'})

    if not check_password_hash(current_user.password, input_password):
        return jsonify({'status': 'error', 'message': 'Passwords do not match'})

    # Redirect the user to the login page immediately
    return jsonify({'status': 'success', 'url': url_for('user.login')})
