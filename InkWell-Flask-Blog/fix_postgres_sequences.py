from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    tables = ["users", "posts", "comments"]

    for table in tables:
        db.session.execute(
            text(
                f"""
                SELECT setval(
                    pg_get_serial_sequence('{table}', 'id'),
                    COALESCE((SELECT MAX(id) FROM {table}), 1),
                    true
                )
                """
            )
        )

    db.session.commit()

    print("PostgreSQL ID sequences fixed successfully.")