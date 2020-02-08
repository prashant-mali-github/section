from flask_script import Manager
from models.create_models import CreateUsersCommand
# from API.models.create_models import CreateUsersCommand
from flask.cli import FlaskGroup
from app import create_app,db
# from API.app import create_app,db
from flask_migrate import MigrateCommand

cli = FlaskGroup(create_app=create_app)
manager = Manager(create_app)


manager.add_command('create_models', CreateUsersCommand)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()