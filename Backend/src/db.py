from flask import current_app, g
from flask.cli import with_appcontext

if current_app.config['TESTING'] == False:
	# database is a sqlite file
else:
	# database is the postgresql or the prod database (with url, ...)