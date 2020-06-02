from the_app import db
from flask import render_template, redirect, url_for, request, flash
# import requests

from . import site
from apis.contact.models import MessageModel

@site.route('/', methods=['GET'])
def index():
	r"""Main route for home page."""

	return render_template('index.html')

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

			msg = MessageModel(
				name = data['name'],
				email = data['email'],
				phone = phone,
				country = country,
				subject = data['subject'],
				message = data['message']
			)

			db.session.add(msg)
			db.session.commit()

			flash("Message successfully sent.")
			return redirect(url_for('site.contact'))					

		except Exception as error:
			db.session.rollback()
			# print(error)
			flash("An error occurred. Message NOT sent!")
			return redirect(url_for('site.contact'))
			
	return render_template('contact.html')
