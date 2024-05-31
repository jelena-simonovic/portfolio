#!/usr/bin/env python3

import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_wtf.csrf import CSRFProtect
from extensions import db

app = Flask(__name__)
login_manager = LoginManager()
admin = Admin(app, name='Dashboard', template_mode='bootstrap3')
csrf = CSRFProtect()

# Configure Flask app
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
login_manager.login_view = 'main.login'

with app.app_context():
    db.create_all()

# Setup CORS headers
CORS(app)

# Import blueprints and register routes
from app.routes import main_routes
app.register_blueprint(main_routes)

from app.models import User, Project, BlogPost

class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(AdminModelView(Project, db.session))
admin.add_view(AdminModelView(BlogPost, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
    

