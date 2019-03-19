from browser import app
from flask import render_template, url_for
from browser import models


@app.route('/')
def index():
	connectors = models.get_connectors()
	return render_template('index.html', connectors=connectors)
