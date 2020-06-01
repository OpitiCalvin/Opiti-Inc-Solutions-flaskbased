from . import site

from flask import render_template, redirect, url_for, request
import requests

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

			msg = {
				"name": data['name'],
				"email": data['email'],
				"phone": data['phone'],
				"country": data['country'],
				"subject": data['subject'],
				"message": data['message']
			}
			# print(f"msg: {msg}")

			try:
				url = "https://solutions.opiticonsulting.com/api/messages"
				response = requests.post(url, json = msg)
				if response.status_code == 200:
					flash("Message successfully sent.")
					return redirect(url_for('site.contact'))					
				else:
					response.raise_for_status()
			except requests.exceptions.HTTPError as errh:
			    return "An Http Error occurred:" + repr(errh)
			except requests.exceptions.ConnectionError as errc:
			    return "An Error Connecting to the API occurred:" + repr(errc)
			except requests.exceptions.Timeout as errt:
			    return "A Timeout Error occurred:" + repr(errt)
			except requests.exceptions.RequestException as err:
			    return "An Unknown Error occurred" + repr(err)

		except Exception as error:
			# db.session.rollback()
			print(error)
			flash("An error occurred.")
			return redirect(url_for('site.contact'))
			
	return render_template('contact.html')
