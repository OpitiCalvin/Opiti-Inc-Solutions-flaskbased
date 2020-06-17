from the_app import db
# from the_app import login_manager
from apis.contact.models import MessageModel, MessageSchema, MessageQuerySchema
from . import admin
from datetime import datetime
from flask import (
	make_response, flash, current_app, redirect, render_template, request, session, url_for, jsonify
)
from flask_login import login_required, login_user, current_user, logout_user
from admin.forms.auth_forms import RegisterForm, LoginForm


messages_query_schema = MessageQuerySchema(many=True)
message_query_schema = MessageQuerySchema()

@admin.route('messages', methods=['GET', 'POST'])
@login_required
def view_messages():
	r"""

	"""

	if request.method == 'POST':
		data = request.json
		# print(f"request data= {data}")
		if "message_id" in data.keys():
			messageData = MessageModel.query.filter_by(message_id = int(data["message_id"])).first()
			if messageData:
				messageData.is_read = True
				db.session.commit()
				message = [message_query_schema.dump(messageData)]
				# print(message)
				return jsonify({'message': 'Query for message successful.', 'data': message})
			
			else:
				return jsonify('No message record found.'),404
		else:
			message = None
			return jsonify('No message record found.'),404
	
	if current_user.role_id == 1:

		messages = messages_query_schema.dump(MessageModel.query.all())
		# print(messages)

		# return render_template('messages/view_all_messages.html', messages = messages)
	else:
		# print(current_user.role_id)
		messages = None
	
	return render_template('messages/view_all_messages.html', messages = messages)

@admin.route('messages/mark_message_as_unread', methods=['POST'])
@login_required
def mark_message_as_unread():
	r"""

	"""

	if request.method == 'POST':
		data = request.json
		# print(data)

		if 'message_id' in data.keys():
			messageData = MessageModel.query.filter_by(message_id = int(data["message_id"])).first()
			if messageData:
				messageData.is_read = False
				db.session.commit()
				
				return jsonify('Message successfully marked as unread.')
			
		return jsonify('Request could not be processed'),400

@admin.route('messages/delete_message', methods=['POST'])
@login_required
def delete_message():
	r"""

	"""

	if request.method == "POST":
		data = request.json
		if "message_id" in data.keys():
			message = MessageModel.query.filter_by(message_id = data['message_id']).first()
			if message:
				db.session.delete(message)
				db.session.commit()

				return jsonify("Message deleted successfully")
			else:
				return jsonify("No message recourd found"),404

		else:
			return jsonify("No message identifier provided. Message deletion cancelled."),400