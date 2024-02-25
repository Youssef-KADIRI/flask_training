from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, DateField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pharmacies.models import User


class RegisterForm(FlaskForm):

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError(message="Email already registered")

    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=20)])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')],
                        validators=[DataRequired()])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),
                                                                     EqualTo('password', message='Passwords must match')
                                                                     ])
    submit = SubmitField('Register your account')


class LoginForm(FlaskForm):

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError(message="Incorrect email or password")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if not user or not user.check_password(password.data):
            raise ValidationError(message="Incorrect email or password")

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddCityForm(FlaskForm):
    name = StringField('City', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Add')


class EditCityForm(FlaskForm):
    name = StringField('City', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Edit')


class DeleteCityForm(FlaskForm):
    submit = SubmitField('Delete')


class AddAreaForm(FlaskForm):
    name = StringField('Area', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Add')


class EditAreaForm(FlaskForm):
    name = StringField('Area', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Edit')


class DeleteAreaForm(FlaskForm):
    submit = SubmitField('Delete')
