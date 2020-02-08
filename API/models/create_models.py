from flask_script import Command

from app import db

class CreateUsersCommand(Command):

    def run(self):
        create_users()
        print('tables created.')

def create_users():
    """ Create users """
    # Create all tables if not exists
    db.create_all()
    db.session.commit()
