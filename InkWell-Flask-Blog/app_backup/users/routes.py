from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from app import db
from app.models import User, Post
from app.forms import UpdateAccountForm
from app.utils import save_image, delete_image

users_bp = Blueprint("users", __name__)


@users_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm(current_user)
    if form.validate_on_submit():
        if form.picture.data:
            delete_image(current_user.profile_image, "UPLOAD_FOLDER_PROFILE")
            current_user.profile_image = save_image(form.picture.data, "UPLOAD_FOLDER_PROFILE", (300, 300))

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash("Your account has been updated.", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio

    return render_template("account.html", title="Account Settings", form=form)


@users_bp.route("/author/<string:username>")
def author_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
    return render_template("author.html", title=user.username, user=user, posts=posts)
