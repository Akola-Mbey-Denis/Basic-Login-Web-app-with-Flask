import os
from flask import Flask
from Model import db,User 
from flask_login import LoginManager,login_user
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from Email import mail
from flask_migrate import Migrate
migrate = Migrate()
 

def create_app():
    '''
    This function creates our flask application instance and loads in all environment dependencies
  
    '''
    app = Flask(__name__, template_folder="templates", static_folder="static")
  
    db.get_app(app)
    login_manager=LoginManager()
    login_manager.login_view='admin.login_admin'
    login_manager.init_app(app)
    
    

    @login_manager.user_loader
    def load_user(email):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.find_user_by_email(email=email)

    app.config.from_object(Configuration)
    db.init_app(app)
    
    migrate.init_app(app, db)
    mail.init_app(app)

    # major blueprints for routing
    from main import admin as admin_blue_print
    
    app.register_blueprint(admin_blue_print)
     
    from auth import email as email_blue_print
    app.register_blueprint(email_blue_print)
    
    return app

# Database migration settings

 