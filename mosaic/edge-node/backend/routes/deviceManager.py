from flask import Blueprint, request
from main import g, users, app, orm, redis

device_blueprint = Blueprint('deviceManager', __name__)

@device_blueprint.route("<string:deviceName>", methods=["POST"])
def newDevice(deviceName):
    try:
        if not g.user or g.user.role < 50:
            return ("Unauthorized", 403)
        ip = request.get_json()["ip"]
        secret = request.get_json()["secret"]
        if g.user and g.user.role >= 50:
            orm.addDevice(deviceName, secret, ip)
            return ("Ok", 200)
        else:
            return ("Unauthorized", 403)
    except Exception as e:
        app.logger.warning(e.__str__())
        return ("bad request", 400)


@device_blueprint.route("<string:deviceName>", methods=["DELETE"])
def delDevice(deviceName):
    if g.user and g.user.role >= 50:
        if orm.findDevice(deviceName):
            orm.delDevice(deviceName)
            return ("Ok", 200)
        return ("not found", 404)
    else:
        return ("Unauthorized", 403)


@device_blueprint.route("<string:deviceName>/join/<string:unitName>", methods=["POST"])
def joinUnit(deviceName, unitName):
    query = None
    # query = g.user and orm.checkPermission(g.user.name, groupName)
    if g.user and (g.user.role >= 50 or (query and query.role == 2)):
        try:
            if orm.findDevice(deviceName) and orm.findUnit(unitName):
                orm.joinUnit(unitName, deviceName)
                return ("Ok", 200)
            else:
                return("Object not founds.", 404)
        except Exception as e:
            return (e.__str__()+"\nMost likely duplicate.", 400)
    else:
        return ("Unauthorized", 403)

@device_blueprint.route("<string:deviceName>/leave/<string:unitName>", methods=["POST"])
def leaveUnit(deviceName, unitName):
    query = None
    # query = g.user and orm.checkPermission(g.user.name, groupName)
    # app.logger.info(g.user.role)
    # return ("ok",200)
    if g.user and (g.user.role >= 50 or (query and query.role == 2)):
        try:
            if orm.findDevice(deviceName) and orm.findUnit(unitName):
                orm.leaveUnit(unitName, deviceName)
                return ("Ok", 200)
            else:
                return("Object not founds.", 404)
            return ("Ok", 200)
        except Exception as e:
            return(e.__str__()+"\nMost likely object not found.", 400)
    else:
        return ("Unauthorized", 403)

@device_blueprint.route("<string:deviceName>/heartbeat", methods=["POST"])
def heartbeat(deviceName):

    ip = request.get_json()["ip"]
    secret = request.get_json()["secret"]
    txbitrate = request.get_json()["txbitrate"]
    rssi = request.get_json()["rssi"]
    ssid = request.get_json()["ssid"]
    bssid = request.get_json()["bssid"]

    if orm.findDevice(deviceName).secret != secret:
        return "No", 405

    redis.add_timer(deviceName, ip, secret, txbitrate, rssi, ssid, bssid)
    return "Ok", 200


@device_blueprint.route("getalive", methods=["GET"])
def getalive():
    keys = set()
    for key in redis.db.keys():
        if "_" in key.decode():
            keys.add(key.decode().split("_")[1])
    res = []
    for key in keys:
        res.append({"devicename": key,
            "ip": redis.db["ip_%s" % key].decode(),
            "txbitrate": redis.db["txbitrate_%s" % key].decode(),
            "rssi": redis.db["rssi_%s" % key].decode(),
            "ssid": redis.db["ssid_%s" % key].decode(),
            "bssid": redis.db["bssid_%s" % key].decode()})

    return {"devices": res}, 200


@device_blueprint.route("getdevice", methods=["GET"])
def getdevice():
    device_list = []
    for device in orm.listAllDevices():
        status = False
        # check if device online
        keys = set()
        for key in redis.db.keys():
            if "_" in key.decode():
                keys.add(key.decode().split("_")[1])
        if device.name in keys:
            status = True

        device = {
            "deviceId": device.deviceId,
            "name": device.name,
            "secret": device.secret,
            "ip": device.ip,
            "status": status
        }
        device_list.append(device)

    return {"devices": device_list}, 200