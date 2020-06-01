from the_app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from apis.contact.models import MessageModel

app = create_app()
migrate = Migrate(app,db, compare_type=True)
manager = Manager(app)

manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=3000, threaded=True))

if __name__ == '__main__':
	manager.run()