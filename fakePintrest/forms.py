from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, equal_to, length, ValidationError
from fakePintrest.models import User

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), length(6, 16)])
    submit = SubmitField("Submit")

class FormSignUp(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), length(6, 16)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), equal_to("password")])
    confirm_btn = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("E-mail registred already")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username registred already")

class FormPhoto(FlaskForm):
    foto = FileField("photo", validators=[DataRequired()])
    confirm_btn = SubmitField("Send")