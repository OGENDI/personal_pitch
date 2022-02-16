from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail
from flask_simplemde import SimpleMDE

import  dateutil.parser

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
db= SQLAlchemy() # initialize database and assign it to db
uploads = UploadSet('photos',IMAGES)
mail = Mail()
simple = SimpleMDE()



def create_app(config_name):
    app = Flask(__name__)
    
    #app configurations
    app.config.from_object(config_options[config_name])
    
    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)
    
    # Blueprint registration 
    from .main import  root as app_blueprint
    app.register_blueprint(app_blueprint)
    
     # registerring auth Blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
    
    
     # configure UploadSet
    configure_uploads(app,uploads)
    
     # function to format dates
    @app.template_filter('strftime')
    def _jinja2_filter_datetime(date, fmt=None):
        date = dateutil.parser.parse(str(date))
        native = date.replace(tzinfo=None)
        format='%b %d, %Y'
        return native.strftime(format) 
    
    return app
    