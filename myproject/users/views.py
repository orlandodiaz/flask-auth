from flask import Blueprint, render_template, redirect, url_for, flash
from myproject.users.forms import (RegisterForm, LoginForm, RequestPasswordResetForm,
                                   PasswordResetForm, PreferencesForm, PasswordForm)
from flask_login import login_user, logout_user, login_required
from myproject import db
from flask_mail import Message
from myproject import mail
from myproject.users.models import User
from myproject.users.email import threaded_email_send
from flask_login import current_user
from myproject import app
from myproject.users import alert
from flask import request
users = Blueprint('users', __name__, url_prefix='/users')
print(f'NAME IS ${__name__}')


@users.route('/request_verify_email', methods=['GET', 'POST'])
def request_verify_email():
    current_user.send_verification_email()
    alert.info('A verification email has been to the email address specified')
    return redirect(url_for('users.preferences'))


@users.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    form = PreferencesForm()
    if not form.is_prefilled:
        form.prefill(current_user)
    pw_form = PasswordForm()

    user = User.query.filter_by(username=current_user.username).first()

    if form.submit_info.data and form.validate_on_submit():

        user.username = form.username.data
        user.full_name = form.full_name.data
        user.email = form.email.data
        db.session.commit()

        alert.info('Updated personal information')

        return redirect(url_for('users.preferences'))

    if pw_form.submit_password.data and pw_form.validate_on_submit():

        User.set_password(user, pw_form.password.data)
        db.session.commit()

        flash('Password updated')

        return redirect(url_for('users.preferences'))

    return render_template('preferences.html', form=form, pw_form=pw_form)

@users.route('/profile')
@login_required

def profile():
    return render_template('profile.html')


@users.route('/verify/<token>', methods=['GET', 'POST'])
def verify_email(token):

    user = User.verify_email_token(token)

    if user.is_verified:
        flash('Your account has already been verified')
        return redirect(url_for('main.index'))

    if user:
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        alert.info('Your email has been verified')
        return redirect(url_for('main.index'))


@users.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)


@users.route('/request_password_reset', methods=['GET', 'POST'])
def request_password_reset():
    form = RequestPasswordResetForm()

    if form.validate_on_submit():
        print('validated on submit')
        user = User.query.filter_by(email=form.email.data).first()
        print("user {}".format(user))
        if user:
            token = user.get_reset_password_token()
            msg = Message("Complete the registration process",
                          recipients=[user.email],
                          body=render_template('email/reset_pasword.txt', user=user, token=token))
            threaded_email_send(msg)
            alert.info("Email with instructions have been sent to {}. Please check your e-mail.".format(form.email.data))
            return redirect(url_for('users.login'))
        else:
            alert.error('An user with that email does not exist')
            return redirect(url_for('users.login'))

    return render_template("request_reset_password.html", form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()


    if form.validate_on_submit():
        print("Login Form validated")
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            print("request.form['password']", request.form['password'])
            if user.check_password(request.form['password']):
                print(form.remember_me.data)
                print(request.cookies)
                login_user(user, remember=form.remember_me.data)
                alert.info('Successful login')

                if request.args.get('next'):
                    return redirect(request.args.get('next'))
                else:
                    return redirect(url_for('main.index'))
            # flash('Incorrect password', category='danger')
            alert.error("Incorrect Password")

        else:
            alert.error('User does not exist')

        # return redirect(url_for('main.index'))


    alert.info("Welcome! This is a back-end authentication demo. \n Register an account to begin or you could"
               " also login with the username demo with password demo123")

    return render_template("login.html", form=form)



@users.route('/logout', methods=['GET', 'POST'])
def logout():
    if User.is_authenticated:
        logout_user()
        return redirect(url_for('main.index'))


@users.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        user = User(username=form.username.data,
                    email=form.email.data,
                    full_name=form.full_name.data)

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        token = user.get_verify_email_token()

        user.send_verification_email()

        alert.info("A verification email has been sent to {}".format(form.email.data))

        return redirect(url_for('main.index'))

    return render_template("register.html", form=form)


