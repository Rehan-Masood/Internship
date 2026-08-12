from flask import Blueprint, render_template, request

from app.models import Post

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=6, error_out=False)
    posts = pagination.items
    featured_post = posts[0] if page == 1 and posts else None
    grid_posts = posts[1:] if page == 1 and posts else posts

    return render_template(
        "home.html",
        title="Inkwell — Home",
        posts=grid_posts,
        featured_post=featured_post,
        pagination=pagination,
    )


@main_bp.route("/about")
def about():
    return render_template("about.html", title="About Inkwell")
