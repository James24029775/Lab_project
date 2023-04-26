from flask import Flask, g, Response, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template

import flask_cors
import time

from config import *

app = Flask(__name__)
flask_cors.CORS(app)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] =  "mysql+pymysql://{user}:{passwd}@{host}:3306/{database}".format(
#         user = db_user,
#         passwd = db_passwd,
#         host = db_host,
#         database = db_dbName)
# db = SQLAlchemy(app)

from controller import *
redis = redis_controller(app.logger, lambda x: app.logger.info(x + " disconnected! QAQ"))
redis_db = redis.db
# db = redis.db

# from models import *
# orm = database(app.logger)


#! Have problems, not check yet
import routes

#! should modify
# app.register_blueprint(routes.login_blueprint, url_prefix="/login/")
app.register_blueprint(routes.mission_blueprint, url_prefix="/mission/")

# 列印出已註冊的 URL 規則
with app.app_context():
    for rule in app.url_map.iter_rules():
        print(rule)

# app.register_blueprint(routes.tenant_blueprint, url_prefix="/tenant/")
# app.register_blueprint(routes.subscriber_blueprint, url_prefix="/subscriber/")

# app.run()