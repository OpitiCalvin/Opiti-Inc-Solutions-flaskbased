from the_app import create_app
from flask_script import Manager, Shell, Server

app = create_app()
manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port=3000, threaded=True))

if __name__ == '__main__':
	manager.run()