import csv
import io

from flask import Blueprint, render_template, request, redirect, url_for, flash

from app import db
from app.models import Contact, ContactGroup, Suppression
from app.utils.email_utils import normalize_email


contacts_bp = Blueprint("contacts", __name__)


@contacts_bp.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # -----------------------------
        # Get form data
        # -----------------------------
        group_name = request.form.get("group_name", "").strip()
        file = request.files.get("csv_file")

        if not group_name:
            flash("Please enter a group name.", "danger")
            return redirect(url_for("contacts.index"))

        if not file or not file.filename:
            flash("Please select a CSV file.", "danger")
            return redirect(url_for("contacts.index"))

        # -----------------------------
        # Read CSV
        # -----------------------------
        try:
            raw_data = file.stream.read()

            # Excel CSV files are normally UTF-8.
            # utf-8-sig also removes BOM if Excel adds one.
            text = raw_data.decode("utf-8-sig")

        except UnicodeDecodeError:
            flash(
                "Could not read this CSV file. Please save it as UTF-8 CSV.",
                "danger"
            )
            return redirect(url_for("contacts.index"))

        # newline="" is important for CSV parsing
        reader = csv.DictReader(io.StringIO(text, newline=""))

        # -----------------------------
        # Normalize CSV headers
        # -----------------------------
        if not reader.fieldnames:
            flash("CSV file is empty.", "danger")
            return redirect(url_for("contacts.index"))

        # Convert:
        # " name " -> "name"
        # " Email " -> "email"
        original_headers = reader.fieldnames

        normalized_headers = [
            (header or "").strip().lower()
            for header in original_headers
        ]

        # Make DictReader use normalized headers
        reader.fieldnames = normalized_headers

        # -----------------------------
        # Validate required columns
        # -----------------------------
        if "email" not in normalized_headers:
            detected = ", ".join(normalized_headers)

            flash(
                f"CSV must contain an 'email' column. "
                f"Detected columns: {detected}",
                "danger"
            )

            return redirect(url_for("contacts.index"))

        # Name is required because your system needs a contact name.
        if (
            "name" not in normalized_headers
            and "full_name" not in normalized_headers
        ):
            detected = ", ".join(normalized_headers)

            flash(
                "CSV must contain a 'name' column. "
                f"Detected columns: {detected}",
                "danger"
            )

            return redirect(url_for("contacts.index"))

        # -----------------------------
        # Find or create group
        # -----------------------------
        group = ContactGroup.query.filter_by(
            name=group_name
        ).first()

        if not group:
            group = ContactGroup(name=group_name)
            db.session.add(group)
            db.session.commit()

        # -----------------------------
        # Import contacts
        # -----------------------------
        added = 0
        skipped = 0

        for row in reader:

            # Get email
            email_raw = row.get("email", "")

            # Get name from either "name" or "full_name"
            name_raw = (
                row.get("name")
                or row.get("full_name")
                or ""
            )

            email = normalize_email(email_raw)
            name = name_raw.strip()

            # Skip incomplete rows
            if not email or not name:
                skipped += 1
                continue

            # Skip duplicate contact
            existing_contact = Contact.query.filter_by(
                email=email
            ).first()

            if existing_contact:
                skipped += 1
                continue

            # Skip suppressed/unsubscribed email
            suppressed = Suppression.query.filter_by(
                email=email
            ).first()

            if suppressed:
                skipped += 1
                continue

            # Create contact
            contact = Contact(
                name=name,
                email=email,
                group_id=group.id
            )

            db.session.add(contact)

            added += 1

        # -----------------------------
        # Save everything
        # -----------------------------
        db.session.commit()

        # -----------------------------
        # Show result
        # -----------------------------
        if added > 0:

            message = (
                f"{added} contact"
                f"{'s' if added != 1 else ''} imported successfully."
            )

            if skipped > 0:
                message += f" {skipped} row(s) skipped."

            flash(message, "success")

        else:
            flash(
                f"No contacts imported. {skipped} row(s) skipped. "
                "Check that each row has a valid name and email.",
                "warning"
            )

        return redirect(url_for("contacts.index"))

    # -----------------------------
    # GET request
    # -----------------------------
    contacts = (
        Contact.query
        .order_by(Contact.created_at.desc())
        .all()
    )

    groups = (
        ContactGroup.query
        .order_by(ContactGroup.name)
        .all()
    )

    return render_template(
        "contacts.html",
        contacts=contacts,
        groups=groups
    )


# =========================================================
# UNSUBSCRIBE CONTACT
# =========================================================
@contacts_bp.post("/unsubscribe/<int:contact_id>")
def unsubscribe(contact_id):

    contact = Contact.query.get_or_404(contact_id)

    # Mark contact as unsubscribed
    contact.subscribed = False

    # Add email to suppression list if it isn't already there
    if not Suppression.query.filter_by(
        email=contact.email
    ).first():

        db.session.add(
            Suppression(
                email=contact.email,
                reason="Unsubscribed"
            )
        )

    db.session.commit()

    flash(
        "Contact unsubscribed.",
        "success"
    )

    return redirect(url_for("contacts.index"))


# =========================================================
# SUBSCRIBE CONTACT
# =========================================================
@contacts_bp.post("/subscribe/<int:contact_id>")
def subscribe(contact_id):

    contact = Contact.query.get_or_404(contact_id)

    # Mark contact as subscribed again
    contact.subscribed = True

    # Remove the email from the suppression list
    suppression = Suppression.query.filter_by(
        email=contact.email
    ).first()

    if suppression:
        db.session.delete(suppression)

    db.session.commit()

    flash(
        "Contact subscribed.",
        "success"
    )

    return redirect(url_for("contacts.index"))