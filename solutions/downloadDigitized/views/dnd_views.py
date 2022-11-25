from . import dnd

from flask import render_template

@dnd.route("", methods=['GET'])
def dnd_index():
	r"""Application's main page."""

	return render_template("dnd_index.html")