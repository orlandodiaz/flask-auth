from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():

    if not current_user.is_authenticated:
        print('not authenticated')
        return redirect(url_for('users.login'))
    else:
        return redirect(url_for('users.profile'))

    # return render_template('base.html')

