from flask import Blueprint, request
from main import g, users, app, orm

policy_blueprint = Blueprint('policyManager', __name__)

@policy_blueprint.route("add", methods=["POST"])
def addPolicy():
    try:
        if not g.user or g.user.role < 50:
            return ("Unauthorized", 403)
        src = request.get_json()["source"]
        dst = request.get_json()["destination"]
        lim = request.get_json()["limits"]
        orm.addPolicy(src, dst, lim)
        return ("Ok.", 200)
    except Exception as e:
        app.logger.warning(e.__str__())
        return ("bad request", 400)


@policy_blueprint.route("del", methods=["DELETE"])
def delPolicy():
    try:
        if not g.user or g.user.role < 50:
            return ("Unauthorized", 403)
        src = request.get_json()["source"]
        dst = request.get_json()["destination"]
        lim = request.get_json()["limits"]
        orm.delPolicy(src, dst, lim)
        return ("Ok.", 200)
    except Exception as e:
        app.logger.warning(e.__str__())
        return ("bad request", 400)

