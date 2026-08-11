from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    submit = SubmitField("Create Account")

    def validate_username(self, username):
        existing = User.query.filter_by(username=username.data).first()
        if existing:
            raise ValidationError("That username is already taken. Please choose another.")

    def validate_email(self, email):
        existing = User.query.filter_by(email=email.data).first()
        if existing:
            raise ValidationError("That email is already registered. Please log in instead.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio", validators=[Length(max=200)])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Save Changes")

    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user = current_user

    def validate_username(self, username):
        if username.data != self.current_user.username:
            existing = User.query.filter_by(username=username.data).first()
            if existing:
                raise ValidationError("That username is already taken. Please choose another.")

    def validate_email(self, email):
        if email.data != self.current_user.email:
            existing = User.query.filter_by(email=email.data).first()
            if existing:
                raise ValidationError("That email is already registered.")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=140)])
    excerpt = StringField("Short Excerpt (optional, shown on the homepage)", validators=[Length(max=240)])
    content = TextAreaField("Content", validators=[DataRequired()])
    cover_image = FileField("Cover Image (optional)", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Publish")


class CommentForm(FlaskForm):
    content = TextAreaField(
        "Add a comment", validators=[DataRequired(), Length(min=1, max=500)]
    )
    submit = SubmitField("Post Comment")
