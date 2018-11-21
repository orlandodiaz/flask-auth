from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, EqualTo, Email, Length
from myproject.users.models import User


class PreferencesForm(FlaskForm):

    username = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    full_name = StringField("Full name", validators=[DataRequired(), Length(min=3, max=35)])
    email = StringField(validators=[DataRequired(), Email()])
    submit_info = SubmitField()

    @property
    def is_prefilled(self):
        return self.username.data and self.full_name.data and self.email.data

    def prefill(self, user):
        """ Prefills preferences form from passed user object"""
        print('prefilling')
        self.username.data = user.username
        self.full_name.data = user.full_name
        self.email.data = user.email

    # def __init__(self, user, *args, **kwargs):
    #     super(PreferencesForm, self).__init__(*args, **kwargs)
    #     print('running')
    #     self.username.data = user.username
    #     self.full_name.data = user.full_name
    #     self.email.data = user.email


class PasswordForm(FlaskForm):
    current_password = PasswordField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    password2 = PasswordField('Repeat your password',
                              validators=[DataRequired(),
                                          EqualTo('password', message="Passwords do not match")])
    submit_password = SubmitField()


class PasswordResetForm(FlaskForm):
    password = PasswordField(validators=[DataRequired()])

    password2 = PasswordField('Repeat your password',
                              validators=[DataRequired(),
                                          EqualTo('password', message="Passwords do not match")])

    submit = SubmitField()


class RequestPasswordResetForm(FlaskForm):

    email = StringField(validators=[DataRequired(), Email()])

    submit = SubmitField("Reset password")

    # @staticmethod
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if not user:
    #         raise ValidationError('An user with that email does not exist. Please enter a valid email')


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])


    remember_me = BooleanField("Remember me")

    submit = SubmitField()


class RegisterForm(FlaskForm):

    username = StringField(validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=35)])
    password2 = PasswordField('Enter your password one more time',
                              validators=[DataRequired(), Length(min=6, max=35), EqualTo('password')])

    full_name = StringField("Full name", validators=[DataRequired(), Length(min=3, max=35)])

    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField()

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already in use.')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail is already in use.')




