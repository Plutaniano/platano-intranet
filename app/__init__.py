from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)
app.config.from_pyfile('config.py')

from .models import db
db.app = app
db.init_app(app)
db.create_all()


login_manager.init_app(app)

from .views import views
app.register_blueprint(views)
