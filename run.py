from app import app
from app.users.models import db
from app.users.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}