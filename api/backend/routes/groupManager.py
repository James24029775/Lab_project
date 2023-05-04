from flask import Blueprint, request
from main import g, app, redis_db, redis, conn
import json
import time

group_blueprint = Blueprint('groupManager', __name__)

# @group_blueprint.route("<string:groupName>", methods=["POST"])
# def addGroup(groupName):
#     if g.user and g.user.role >= 50:
#         if orm.findGroup(groupName):
#             return ("Conflict", 409)
#         orm.addGroup(groupName)
#         return ("Ok", 200)
#     else:
#         return ("Unauthorized", 403)

# @group_blueprint.route("<string:groupName>", methods=["DELETE"])
# def delGroup(groupName):
#     if g.user and g.user.role >= 50:
#         if orm.findGroup(groupName):
#             orm.delGroup(groupName)
#         return ("Ok", 200)
#     else:
#         return ("Unauthorized", 403)


# @group_blueprint.route("<string:groupName>/devices/<string:deviceName>", methods=["POST"])
# def addDeviceToGroup(groupName, deviceName):
#     if g.user and g.user.role >= 50:
#         if orm.findDevice(deviceName) and orm.findGroup(groupName):
#             try:
#                 orm.addDeviceToGroup(deviceName, groupName)
#             except Exception as e:
#                 return (e.__str__() + "\nMost likely pair duplicates.", 400)
#             return ("Ok", 200)
#         else:
#             return ("Object not found", 404)
#     else:
#         return ("Unauthorized", 403)


# @group_blueprint.route("<string:groupName>/devices/<string:deviceName>", methods=["DELETE"])
# def removeDeviceFromGroup(groupName, deviceName):
#     if g.user and g.user.role >= 50:
#         if orm.findDevice(deviceName) and orm.findGroup(groupName):
#             try:
#                 orm.removeDeviceFromGroup(deviceName, groupName)
#             except Exception as e:
#                 return (e.__str__() + "\nMost likely cannot find object.", 400)
#         return ("Ok", 200)
#     else:
#         return ("Unauthorized", 403)


# @group_blueprint.route("<string:groupName>/operator/<string:userName>", methods=["POST"])
# def grantUser(groupName, userName):
        
#     req = request.get_json()
    
#     if role not in [0, 1, 2] or 'role' not in req: 
#         return ("bad request.", 400)

#     query = orm.checkPermission(g.user.name, groupName)
#     if g.user and (g.user.role >= 50 or (query and query.role == 2)):
#         orm.grantPermission(userName, groupName, req['role'])
#         return ("Ok", 200)
#     else:
#         return ("Unauthorized", 403)


# ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# 原本：
@group_blueprint.route("<string:groupName>/unit/<string:unitName>", methods=["POST"])
def createUnit(groupName, unitName):
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    id = 0
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # query = g.user and orm.checkPermission(g.user.name, groupName)
    # if g.user and (g.user.role >= 50 or (query and query.role == 2)):
    if request.is_json:
        req = request.get_json()
        myself_timer = time.time()
        if 'bitrateLimit' in req:
            # app.logger.info("createUnit", req['bandwidthLimit'])
            redis.addUnit(groupName, unitName, req['bitrateLimit'])
        else:
            redis.addUnit(groupName, unitName, 0)
    else:
        # app.logger.info("createUnit", groupName, unitName)  
        redis.addUnit(groupName, unitName, 0)

    return ("Ok", 200)
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # else:
    #     return ("Unauthorized", 403)

@group_blueprint.route("<string:groupName>/unit/<string:unitName>", methods=["DELETE"])
def deleteUnit(groupName, unitName):
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # query = g.user and orm.checkPermission(g.user.name, groupName)
    # if g.user and (g.user.role >= 50 or (query and query.role == 2)):
    unitId = redis.findUnit(unitName)
    if redis_db.hexists('units', unitId):
        redis_db.hdel('units', unitId)
    return ("Ok", 200)
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # else:
        # return ("Unauthorized", 403)
