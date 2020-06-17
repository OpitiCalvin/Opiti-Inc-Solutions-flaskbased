from the_app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from apis.contact.models import MessageModel
from apis.auth.models.api_users import UserModel
from apis.auth.models.user_roles import RoleModel

app = create_app()
migrate = Migrate(app,db, compare_type=True)
manager = Manager(app)

@manager.command
def seed_user_roles():
	# roleAdmin = RoleModel(
	# 	name = "Administrator",
	# 	description = "User can create, read, update and download records.",
	# 	created_by = "Seeding"
	# )
	# db.session.add(roleAdmin)
	roleCreator = RoleModel(
		name = "User",
		description = "User can create and read records.",
		created_by = "Seeding"
	)
	db.session.add(roleCreator)
	
	db.session.commit()
	print("User roles created successfully.")

@manager.command
def seed_users():	
	#! Creating a ADMIN USER
	if not UserModel.query.filter_by(username="Admin").first():
		admin_user = UserModel(
			username="Admin",
			email="opiticalvin@gmail.com",
			password=UserModel.generate_hash('M@c1nt0$h'),
			role_id=1,
			created_by="Seeding"
		)
		db.session.add(admin_user)
	else:
		print("Admin user exists, skipping...")

	db.session.commit()
	print("users created successfully")

manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=3000, threaded=True))

if __name__ == '__main__':
	manager.run()