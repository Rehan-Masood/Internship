from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import current_user, login_required

from app import db
from app.models import Post, Comment
from app.forms import PostForm, CommentForm
from app.utils import save_image, delete_image

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        cover_filename = None
        if form.cover_image.data:
            cover_filename = save_image(form.cover_image.data, "UPLOAD_FOLDER_COVER", (1200, 700))

        post = Post(
            title=form.title.data,
            excerpt=form.excerpt.data,
            content=form.content.data,
            cover_image=cover_filename,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Your article has been published!", "success")
        return redirect(url_for("posts.post_detail", post_id=post.id))

    return render_template("create_post.html", title="New Article", form=form, legend="Write a New Article")


@posts_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Please log in to leave a comment.", "info")
            return redirect(url_for("auth.login"))

        comment = Comment(content=comment_form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been posted.", "success")
        return redirect(url_for("posts.post_detail", post_id=post.id) + "#comments")

    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
    return render_template("post.html", title=post.title, post=post, comments=comments, comment_form=comment_form)


@posts_bp.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        if form.cover_image.data:
            delete_image(post.cover_image, "UPLOAD_FOLDER_COVER")
            post.cover_image = save_image(form.cover_image.data, "UPLOAD_FOLDER_COVER", (1200, 700))

        post.title = form.title.data
        post.excerpt = form.excerpt.data
        post.content = form.content.data
        db.session.commit()
        flash("Your article has been updated.", "success")
        return redirect(url_for("posts.post_detail", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.excerpt.data = post.excerpt
        form.content.data = post.content

    return render_template("create_post.html", title="Edit Article", form=form, legend="Edit Article", post=post)


@posts_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    delete_image(post.cover_image, "UPLOAD_FOLDER_COVER")
    db.session.delete(post)
    db.session.commit()
    flash("Your article has been deleted.", "info")
    return redirect(url_for("main.home"))
