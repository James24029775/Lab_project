from flask import Blueprint, request
from main import g, users, app, orm

user_blueprint = Blueprint('auth', __name__)

@user_blueprint.route("/<string:name>/login", methods=["POST"])
def login(name):
    try:
        passwd = request.get_json()["password"]
        token = users.login(name, passwd)
        if token:
            return ({"token": token}, 200)
        else:
            return ("bad authentication", 401)
    except Exception as e:
        app.logger.info(e.__repr__())
        return ("bad request", 400)

@user_blueprint.route("/whoami", methods=["GET"])
def whoami():
    if g.user:
        return ("%s %s" % (g.user.name, g.user.role))
    else:
        return "Unauthenticated"


@user_blueprint.route("/<string:name>", methods=["POST"])
def addUser(name):
    if g.user and g.user.role >= 50:
        if orm.findUser(name):
            return ("Already exists", 409)
        passwd = request.get_json()["password"]
        users.addUser(name, passwd, 0)
        return ("Ok.", 200)
    return ("Unauthorized", 403)

@user_blueprint.route("/<string:name>/passwd", methods=["POST"])
def passwd(name):
    if g.user:
        passwd = request.get_json()["password"]
        target = orm.findUser(name)
        if not target:
            return ("Object not exists", target)
        if target == g.user or g.user.role > target.role:
            users.passwd(name, passwd)
            return ("Ok.", 200)
        else:
            return ("Unauthorized", 403)
    else:
        return ("Unauthenticated",401)

@user_blueprint.route("/<string:name>/set/<string:role>", methods=["POST"])
def setRole(name, role):
    role = int(role)
    if not 0 <= role <= 100:
        return ("Invalid role.", 400)
    if g.user:
        target = orm.findUser(name)
        if not target:
            return ("Object not exists", 404)
        if g.user.role > max(role, target.role):
            target.setRole(role)
            return ("Ok.", 200)
        else:
            return ("Unauthorized", 403)
    else:
        return ("Unauthenticated",401)
