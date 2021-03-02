
from dotenv import load_dotenv
from flask import Flask 

load_dotenv()
#application factory 
def create_app(test_config=None):
	#create and configure the app
	app = Flask(__name__,instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev')

	if test_config is None:
		#load the instance config, if it exists, when not test
		app.config.from_pyfile('config.py',silent=True)

	else:
		#load the test config if passed in 
		app.config.from_mapping(test_config)
	#ensure the instance foler exists
	# try:
	# 	os.makedirs(app.instance_path)
	# except OSError:
	# 	pass
		

	from . import db 
	db.init_app(app)

	from . import auth 
	app.register_blueprint(auth.bp)

	from . import blog 
	app.register_blueprint(blog.bp) 
	app.add_url_rule('/',endpoint='index')

	return app 

