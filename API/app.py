from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(main=True):

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/section_db'
    app.config['SECRET_KEY'] = 'dev'
    app.config['DEBUG'] = True

    CORS(app, supports_credentials=True)
    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Marshmallow
    ma.init_app(app)

    # Setup Swagger
    # swagger.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)


    from roles.urls import roles_api
    app.register_blueprint(roles_api, url_prefix='/api')

    from sections.urls import section_api
    app.register_blueprint(section_api, url_prefix='/api')

    from operations.urls import operation_api
    app.register_blueprint(operation_api, url_prefix='/api')

    from rolesconfig.urls import roles_config_api
    app.register_blueprint(roles_config_api, url_prefix='/api')

    return app
