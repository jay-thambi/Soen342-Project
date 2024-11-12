from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config
from .models import db, User
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirect to login page if not authenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
from .routes.auth_routes import auth_bp
from .routes.admin_routes import admin_bp
from .routes.client_routes import client_bp
from .routes.instructor_routes import instructor_bp

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(client_bp, url_prefix='/client')
app.register_blueprint(instructor_bp, url_prefix='/instructor')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
