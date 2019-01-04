from myproject import app
from myproject.users.models import db
from myproject.users.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


if __name__ == '__main__':
    app.run()
