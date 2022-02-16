from app import create_app
from flask_script import Manager,Server
from app import db
from app.models import Upvotes, User
from app.models import Pitches
from app.models import Downvotes
from app.models import Comments
from flask_migrate import Migrate, MigrateCommand

# creating app instance
# app = create_app('development')
app = create_app('production') # goherood for local production << deactivate or comment when on development mode>>


manager = Manager(app)
manager.add_command('server',Server)

# initialize migrate class that has been imported
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(
                   app = app,db = db,User = User,
                   Pitches=Pitches,Comments=Comments,
                   Downvotes=Downvotes, Upvotes=Upvotes
               )


if __name__ == '__main__':
    
    manager.run()