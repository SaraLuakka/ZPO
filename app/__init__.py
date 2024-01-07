import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # app.config['DEBUG'] = True

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Login = system_ewidencji
    # Haslo = to_jest_system_ewidencji
    # DB name = system_ewidencji
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://system_ewidencji:to_jest_system_ewidencji@localhost/system_ewidencji?charset=utf8mb4'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    # Blueprint main
    from app.views import bp as main_bp
    app.register_blueprint(main_bp)

    # Blueprint auth
    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    # Blueprint category
    from app.category import category as category_bp
    app.register_blueprint(category_bp)

    # Blueprint hashtag
    from app.hashtag import hashtag as hashtag_bp
    app.register_blueprint(hashtag_bp)

    # Blueprint task
    from app.task import task as task_bp
    app.register_blueprint(task_bp)

    # Blueprint achievement
    from app.achievement import achievement as achievement_bp
    app.register_blueprint(achievement_bp)

    # Blueprint rating
    from app.rating import rating as rating_bp
    app.register_blueprint(rating_bp)

    return app