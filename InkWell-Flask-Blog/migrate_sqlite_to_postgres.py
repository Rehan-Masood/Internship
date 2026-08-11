"""Optional one-time helper to copy data from SQLite into PostgreSQL.

Usage:
    set DATABASE_URL=...\n+    set SQLITE_DATABASE_PATH=app/site.db\n+    python migrate_sqlite_to_postgres.py
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app, db
from app.models import User, Post, Comment


def main():
    sqlite_path = os.environ.get("SQLITE_DATABASE_PATH", os.path.join("app", "site.db")).replace("\\", "/")
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is required for migration.")

    sqlite_engine = create_engine(f"sqlite:///{sqlite_path}")
    sqlite_session = sessionmaker(bind=sqlite_engine)()

    app = create_app()
    with app.app_context():
        db.create_all()

        existing_users = {user.id for user in User.query.all()}
        existing_posts = {post.id for post in Post.query.all()}
        existing_comments = {comment.id for comment in Comment.query.all()}

        for row in sqlite_session.query(User).all():
            if row.id in existing_users:
                continue
            db.session.merge(
                User(
                    id=row.id,
                    username=row.username,
                    email=row.email,
                    password_hash=row.password_hash,
                    bio=row.bio,
                    profile_image=row.profile_image,
                    date_joined=row.date_joined,
                )
            )

        for row in sqlite_session.query(Post).all():
            if row.id in existing_posts:
                continue
            db.session.merge(
                Post(
                    id=row.id,
                    title=row.title,
                    content=row.content,
                    excerpt=row.excerpt,
                    cover_image=row.cover_image,
                    date_posted=row.date_posted,
                    date_updated=row.date_updated,
                    user_id=row.user_id,
                )
            )

        for row in sqlite_session.query(Comment).all():
            if row.id in existing_comments:
                continue
            db.session.merge(
                Comment(
                    id=row.id,
                    content=row.content,
                    date_posted=row.date_posted,
                    user_id=row.user_id,
                    post_id=row.post_id,
                )
            )

        db.session.commit()


if __name__ == "__main__":
    main()