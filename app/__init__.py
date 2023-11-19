from flask import Flask
from app.extensions import db
from config import Config
from flask_login import LoginManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 这里随便硬编码一个Flask密钥，使程序跑起来。正统做法是把它写在环境变量里，
    # 并使用SECRET_KEY = os.environ.get('SECRET_KEY')读取。
    # 详见config.py文件
    app.secret_key = 'your_random_secret_key'

    # Initialize Flask extensions here
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models.auth import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints here
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.pet_profile import bp as pet_bp
    app.register_blueprint(pet_bp)

    return app