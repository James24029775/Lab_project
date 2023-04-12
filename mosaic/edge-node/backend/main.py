from flask import Flask, g, Response, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, render_template

import flask_cors
import time

from config import *

app = Flask(__name__)
flask_cors.CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =  "mysql+pymysql://{user}:{passwd}@{host}:3306/{database}".format(
        user = db_user,
        passwd = db_passwd,
        host = db_host,
        database = db_dbName)
db = SQLAlchemy(app)

from controller import *
from models import *

orm = database(app.logger)
redis = redis_controller(app.logger, lambda x: app.logger.info(x + " disconnected! QAQ"))
users = user_controller(app.logger, orm, jwt_secret)
devices = device_controller(app.logger, orm)

import routes


app.register_blueprint(routes.user_blueprint, url_prefix="/auth/")
app.register_blueprint(routes.device_blueprint, url_prefix="/device/")
app.register_blueprint(routes.group_blueprint, url_prefix="/group/")
app.register_blueprint(routes.exporter_blueprint, url_prefix="/exporter/")
app.register_blueprint(routes.policy_blueprint, url_prefix="/policy/")

### test redis ###
# redis.add_timer("owo")
# time.sleep(3)
# redis.add_timer("owo")

### test orm ###
# orm.addDevice("LinLee", "abc123", 1)
# orm.addUser("qwq", "qaq", 0);
# orm.addGroup("qwq");
# orm.findUser("qwq").first().name

### test user controller ###
# users.addUser("owo", "qaq", 70)
# app.logger.warning(users.authenticate(str(users.login("owo", "qaq"))))
# app.logger.warning(str(users.login("owo", "qaqq")))

### test device controller ###
# devices.addDevice("Lin-OwO-1", "abc123", "10.0.0.1")
# devices.addDevice("Lin-OwO-2", "abc456", "10.0.0.2")
# devices.addGroup("Lin-OwO")
# devices.addDeviceToGroup("Lin-OWO-1", "Lin-OwO")
# devices.addDevice2Group("Lin-OWO-2", "Lin-OwO")
# devices.removeDeviceFromGroup("Lin-OWO-1", "Lin-OWO")
# devices.removeDeviceFromGroup("Lin-OWO-2", "Lin-OWO")
# devices.addRole("Lin-OWQ", "Lin-Lee", 2)
# device.grantPermission("
# devices.grantPermission("owo", "Lin-OWO", 1)
# app.logger.info(devices.authorize("owo", "Lin-OWO"))
