from the_app import db
# from the_app import login_manager
from apis.auth.models.api_users import UserModel, UserQuerySchema
from apis.auth.models.user_roles import RoleModel, RoleQuerySchema
from . import admin
from datetime import datetime
from flask import (
	make_response, flash, current_app, redirect, render_template, request, session, url_for, jsonify
)
from flask_login import login_required, login_user, current_user, logout_user
from admin.forms.auth_forms import RegisterForm, LoginForm


users_query_schema = UserQuerySchema(many=True)
user_query_schema = UserQuerySchema()
roles_query_schema = RoleQuerySchema(many=True)
role_query_schema = RoleQuerySchema()

@admin.route('', methods=['GET'])
def admin_index():
	return render_template('admin_index.html')

@admin.route('/auth/roles', methods=['GET'])
@login_required
def view_roles():
	roles = roles_query_schema.dump(RoleModel.query.all())
	# print(roles)
	return render_template('auth/view_roles.html', roles = roles)

@admin.route('/auth/roles/<role_id>', methods=['GET', 'PUT'])
@login_required
def view_a_role(role_id):
	if current_user.role_id ==1:
		role = role_query_schema.dump(RoleModel.query.filter_by(role_id=int(role_id)).first())
	else:
		role = None
		# print(role)
	return render_template('auth/view_a_role.html', role = role)

@admin.route('/auth/roles/<role_id>', methods=['GET', 'POST'])
@login_required
def update_a_role(role_id):
	if current_user.role_id ==1:
		if request.method == 'POST':
			data = request.form

			role = RoleModel.query.filter_by(role_id=int(role_id)).first()
			if not role_id:
				flash(f"Role of ID {role_id} does not exist.")
				return redirect(url_for('admin.view_roles'))
			try:
				if data['description'] != '' and data['description'] != role.description:
					role.description = data['description']
					role.updated_by = current_user.username

					db.session.commit()

					flash("User role record successfully updated.")
					return redirect(url_for('admin.view_roles'))
			except Exception as e:
				db.session.rollback()
				flash(f"Update unsuccessful. ERROR: {e.args}")
				return redirect(url_for('admin.view_roles'))

@admin.route('/services/delete_role', methods=['GET', 'POST'])
@login_required
def delete_role():
	r"""
	"""

	if request.method == 'POST':
		data = request.json
		# print(f"Data to delete = {data}")
		if current_user.role_id == 1:
			try:
				role = RoleModel.query.filter_by(role_id = data['role_id']).first()
				if not role:
					flash(f"Role record was not found.")
					return redirect(url_for('admin.view_roles'))

				db.session.delete(role)
				db.session.commit()

				return jsonify("Role successfully deleted.")

			except Exception as e:
				db.session.rollback()
				flash(f"Deletion task unsuccessful. ERROR: {e.args}")
				return redirect(url_for('admin.view_roles'))

# @admin.route('/services/undelete_role', methods=['GET', 'POST'])
# @login_required
# def undelete_role():
# 	r"""
# 	"""

# 	if request.method == 'POST':
# 		data = request.json
# 		# print(f"Data to undelete = {data}")
# 		if current_user.role_id == 1:
# 			try:
# 				role = RoleModel.query.filter_by(role_id = data['role_id']).first()
# 				if not role:
# 					flash(f"Role record was not found.")
# 					return redirect(url_for('admin.view_roles'))

# 				# TO DO: Change to soft delete
# 				role.deleted = False
# 				role.deleted_by = None
# 				role.deleted_date = None

# 				# db.session.delete(user_roles)
# 				db.session.commit()

# 				return jsonify("Role successfully undeleted.")

# 			except Exception as e:
# 				db.session.rollback()
# 				flash(f"Undo deletion task unsuccessful. ERROR: {e.args}")
# 				return redirect(url_for('admin.view_roles'))

@admin.route('/auth/login', methods=['GET','POST'])
def user_login():

	if current_user.is_authenticated:
		flash("User already logged! Redirecting...")
		return redirect(url_for('admin.admin_index'))

	form = LoginForm()
	if request.method=="POST" and form.validate_on_submit():
		user = UserModel.find_by_username(form.username.data)
		if not user:
			user = UserModel.find_by_email(form.username.data)
			if not user:
				flash("ACCESS DENIED: Invalid Credentials.")
				return redirect(url_for('admin.user_login'))

		if UserModel.verify_hash(user.password, form.password.data):
			user.authenticated = True
			user.last_log_in = user.current_logged_in
			user.current_logged_in = datetime.now()
			# db.session.add(user)
			db.session.commit()
			# print(form.remember_me.data)
			if form.remember_me.data:
				login_user(user, remember=form.remember_me.data)
			else:
				login_user(user, remember=False)
			flash("Login successful...")
			return redirect(url_for('admin.view_messages'))

		else:
			flash("ACCESS DENIED: Invalid Credentials.")

	return render_template('auth/user_login.html', form=form)

@admin.route('/auth/logout', methods=['GET'])
@login_required
def user_logout():
	r"""
	"""

	user = current_user
	user.authenticated = False
	# db.session.add(user)
	db.session.commit()

	logout_user()
	flash("User successfully logged out.")
	return redirect(url_for('admin.admin_index'))

@admin.route('/auth/users', methods=['GET'])
@login_required
def view_users():
	r"""

	"""
	if current_user.role_id == 1:
		users = users_query_schema.dump(UserModel.query.all())
		# print(users)
	else:
		users = [user_query_schema.dump(UserModel.find_by_username(username = current_user.username))]

	return render_template('auth/view_users.html', users = users)

@admin.route('/auth/users/<user_id>', methods=['GET', 'PUT'])
@login_required
def view_a_user(user_id):
	r"""

	"""

	
	roles_data = RoleModel.query.all()
	roles = {str(item.role_id): item.name for item in roles_data}
	
	if current_user.role_id == 1:
		user = user_query_schema.dump(UserModel.query.filter_by(user_id = int(user_id)).first())
	elif current_user.user_id == user_id:
		user = user_query_schema.dump(UserModel.query.filter_by(user_id = int(user_id)).first())
	else:
		user = None

	# print(user)
	
	return render_template('auth/view_user.html', user = user, roles=roles)

@admin.route('/auth/users/<user_id>', methods=['GET', 'POST'])
@login_required
def update_a_user(user_id):
	r"""

	"""

	if request.method == 'POST':
		data = request.form
		# print(data)

		roles_data = RoleModel.query.all()
		roles = {str(item.role_id): item.name for item in roles_data}		
		
		for key, val in roles.items():
			if val == data['role_name']:
				role_id = key

		if role_id < current_user.role_id:
			flash("You cannot assign a higher role than your own. Contact system administrator for that.")
			return redirect(url_for('admin.view_users'))

		if current_user.role_id == 1:
			user = UserModel.query.filter_by(user_id=int(user_id)).first()
			if not user:
				flash(f"User record with id {user_id} not found.")
				return redirect(url_for('admin.view_users'))

			try:
				user.email = data['email']
				user.role_id = role_id
				user.updated_by = current_user.username

				db.session.commit()
			except Exception as e:
				db.session.rollback()
				print(f"An error occurred: \n {str(e)}")
				flash("Internal Server error")

			flash("User information successfully updated.")
			return redirect(url_for('admin.view_users'))

@admin.route('/auth/users/add', methods=['GET', 'POST'])
@login_required
def create_user():
	r"""

	"""
	
	form = RegisterForm()
	if request.method == 'POST' and form.validate_on_submit():
		if current_user.role_id == 1:
			data = request.form
			# print(data)

			try:
				user = UserModel(
					email = data['email'],
					username = data['username'],
					password = UserModel.generate_hash(data['password']),
					role_id = int(2),
					created_by = current_user.username
				)

				db.session.add(user)
				db.session.commit()

				flash("user created successfully.")

				return redirect(url_for('admin.view_users'))
			except Exception as e:
				db.session.rollback()
				flash(f"User record not created. Error: {e.args}")
				return redirect(url_for('admin.create_user'))
		else:
			flash("You do not have the right credentials to create a user.")
			return redirect(url_for('admin.view_users'))
	
	return render_template('auth/create_users.html', form=form)

@admin.route('/services/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
	if request.method == 'POST':
		data = request.json
		# print(f"Data to delete = {data}")
		if current_user.role_id == 1:
			try:
				user = UserModel.query.filter_by(email = data['email']).first()
				if not user:
					flash(f"User record for email {data['email']} not found.")
					return redirect(url_for('admin.view_users'))

				if user.role_id <= 2 and current_user.role_id != 1:
					flash("Super administrative rights are required to delete this record.")
					return redirect(url_for('admin.view_users'))

				# # TO DO: Change to soft delete
				# user.deleted = True
				# user.deleted_by = current_user.username
				# user.deleted_date = datetime.now()

				db.session.delete(user)
				db.session.commit()

				return jsonify("User successfully deleted.")

			except Exception as e:
				db.session.rollback()
				flash(f"Deletion task unsuccessful. ERROR: {e.args}")
				return redirect(url_for('admin.view_users'))

# @admin.route('/services/undelete_user', methods=['GET', 'POST'])
# @login_required
# def undelete_user():
# 	if request.method == 'POST':
# 		data = request.json
# 		# print(f"Data to undelete = {data}")
# 		if current_user.role_id == 1:
# 			try:
# 				user = UserModel.query.filter_by(email = data['email']).first()
# 				if not user:
# 					flash(f"User record for email {data['email']} not found.")
# 					return redirect(url_for('admin.view_users'))

# 				# if user.role_id <= 2 and current_user.role_id != 1:
# 				# 	flash("Super administrative rights are required to delete this record.")
# 				# 	return redirect(url_for('admin.view_users'))

# 				# TO DO: Change to soft delete
# 				user.deleted = False
# 				user.deleted_by = None
# 				user.deleted_date = None

# 				# db.session.delete(user_roles)
# 				db.session.commit()

# 				return jsonify("User successfully Restored.")

# 			except Exception as e:
# 				db.session.rollback()
# 				flash(f"Restoration task unsuccessful. ERROR: {e.args}")
# 				return redirect(url_for('admin.view_users'))

@admin.route('/services/email-check', methods=['GET', 'POST'])
def checkEmailUniqueness():
	r"""
	"""

	if request.method == 'POST':
		if 'email' in request.json:
			email = request.json['email']
			# print(email)

		users = UserModel.query.all()
		emails = [user.email for user in users]
		# print(emails)
		if email in emails:
			return jsonify('<span style=\'color:red;\'>Email already in use! Please try another.</span>'), 200
			# return True
		else:
			return jsonify('<span style=\'color:green;\'>Email entry is alright.</span>'), 200
