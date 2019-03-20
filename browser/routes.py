from browser import app
from flask import render_template, request, jsonify, flash
from browser import models
from browser.forms import ServerCredentialForm
from browser import models


@app.route('/', methods=['GET', 'POST'])
def index():
	connectors = models.get_connectors()
	form = ServerCredentialForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			server = form.server.data
			servername = form.servername.data
			username = form.username.data
			password = form.password.data
			app.logger.info('------------------- Form Data -----------------------------')
			app.logger.info(servername)
			app.logger.info(username)
			app.logger.info(password)
			app.logger.info(form.validate())
			app.logger.info(form.errors)
			databases = None
			try:
				databases = models.get_databases(server, servername, username, password)
			except:
				return '<div class="alert alert-danger"><strong>Error: </strong>Login Failed</div>'
			app.logger.info(databases['Database_Name'].to_list())
			return jsonify(status='ok', databases=databases['Database_Name'].to_list())
		else:
			return '<div class="alert alert-danger"><strong>Error: </strong>Data Required!</div>'
	return render_template('index.html', connectors=connectors, form=form)


@app.route('/get_table', methods=['GET'])
def get_table():
	server = request.args.get('server')
	servername = request.args.get('servername')
	username = request.args.get('username')
	password = request.args.get('password')
	db_name = request.args.get('db_name')

	tables = None
	try:
		tables = models.get_table(server, servername, db_name, username, password)
		tables = tables['Table_Name'].to_list()
	except:
		return jsonify({'Error': 'Could Not Load Tables'})
	return jsonify(tables=tables)

@app.route('/get_records', methods=['GET'])
def get_records():
	server = request.args.get('server')
	servername = request.args.get('servername')
	username = request.args.get('username')
	password = request.args.get('password')
	db_name = request.args.get('db_name')
	table_name = request.args.get('table_name')

	records = None
	try:
		records = models.get_top_records(server, servername, db_name, 'dbo',table_name, username, password)
		records = records.to_html(index=False)
	except:
		return jsonify({'Error': 'Could Not Load Records'})

	return jsonify(html_table=records)

