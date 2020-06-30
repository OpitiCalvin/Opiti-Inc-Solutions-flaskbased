from the_app import db
from flask import render_template, redirect, url_for, request, flash
# import requests

from the_app import login_manager
from apis.auth.models.api_users import UserModel
from . import site
from apis.contact.models import MessageModel

@login_manager.user_loader
def user_loader(user_id):
	r"""
	Given `user_id`, return the associated User object.

	"""

	return UserModel.query.get(user_id)

@site.route('/', methods=['GET'])
def index():
	r"""Main route for home page."""

	# return render_template('index.html')
	return render_template('new_index.html')

@site.route('/new', methods=['GET'])
def new_index():
	r"""Main route for home page."""

	return render_template('new_index.html')


@site.route('/contact', methods=['GET', 'POST'])
def contact():
	r"""Main route for home page."""

	if request.method == 'POST':
		try:
			data = request.form.to_dict()
			# print(data)

			if "phone" in data.keys():
				phone = data["phone"]
			else:
				phone = None

			if "country" in data.keys():
				country = data["country"]
			else:
				country = None
			
			if "country_code" in data.keys():
				country_code = data["country_code"]
			else:
				country_code = None

			msg = MessageModel(
				name = data['name'],
				email = data['email'],
				phone = phone,
				country = country,
				country_code = country_code,
				subject = data['subject'],
				message = data['message']
			)

			db.session.add(msg)
			db.session.commit()

			flash("Message successfully sent.")
			return redirect(url_for('site.contact'))					

		except Exception as error:
			db.session.rollback()
			print(error)
			flash("An error occurred. Message NOT sent!")
			return redirect(url_for('site.contact'))
			
	return render_template('contact.html')
