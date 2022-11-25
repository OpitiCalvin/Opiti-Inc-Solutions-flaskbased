from . import mapper
from flask import render_template

@mapper.route("", methods=["GET"])
def mapper_index():
	r"""Solution's main page."""


	return render_template("mapper_index.html")