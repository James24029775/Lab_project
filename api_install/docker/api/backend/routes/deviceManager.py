from flask import Blueprint, request, jsonify
import time
import json
import uuid
from main import g, app, redis_db, redis, conn

device_blueprint = Blueprint('deviceManager', __name__)

@device_blueprint.route('getalive', methods=['GET'])
def getalive():
    #! 這裡優先處理！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    allDevices = redis.listAllDevices()
    # keys = set()
    # for key in redis.db.keys():
    #     if "_" in key.decode():
    #         keys.add(key.decode().split("_")[1])
    res = []
    for device in allDevices:
        res.append({
            "devicename": device["deviceName"],
            "ip": device["ip"],
            "txbitrate": device["txbitrate"],
            "rssi": device["rssi"],
            "ssid": device["ssid"],
            "bssid": device["bssid"]})
    return {"devices": res}, 200



@device_blueprint.route("<string:deviceName>", methods=["POST"])
def newDevice(deviceName):
    try:
        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        # if not g.user or g.user.role < 50:
        #     return ("Unauthorized", 403)
        # id = request.get_json()["id"]
        ip = request.get_json()["ip"]
        secret = request.get_json()["secret"]
        status = False
        txbitrate = rssi = ssid = bssid = 'N/A'
        timestamp = time.time()
        
        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        # if g.user and g.user.role >= 50:
        redis.addDevice(deviceName, secret, ip, txbitrate, rssi, ssid, bssid, status, timestamp)
        return ("Ok", 200)
        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        # else:
        #     return ("Unauthorized", 403)
    except Exception as e:
        app.logger.warning(e.__str__())
        return ("bad request", 400)
    

@device_blueprint.route("getdevice", methods=["GET"])
def getdevice():
    device_list = []
    devices = redis_db.hgetall('devices')
    for deviceId, deviceData in devices.items():
        status = False
        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        # check if device online
        # keys = set()
        # for key in redis.db.keys():
        #     if "_" in key.decode():
        #         keys.add(key.decode().split("_")[1])
        # if device.name in keys:
        #     status = True

        deviceId = deviceId.decode('utf-8') # 將 bytes 轉換為字串
        deviceData = json.loads(deviceData.decode('utf-8'))
        device = {
            'deviceId': deviceId,
            'name': deviceData.get('deviceName', ''),
            'ip': deviceData.get('ip', ''),
            'secret': deviceData.get('secret', ''),
            'status': status,
            'timestamp': deviceData.get('timestamp', ''),
        }
        device_list.append(device)
    device_list.sort(key=lambda x: float(x['timestamp']), reverse=True)

    return {"devices": device_list}, 200


@device_blueprint.route("<string:deviceName>", methods=["DELETE"])
def delDevice(deviceName):
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # if g.user and g.user.role >= 50:
    return redis.delDevice(deviceName)
    # else:
    #     return ("Unauthorized", 403)


    
    # # 檢查missionid是否存在
    # if redis_db.hexists('missions', missionId):
    #     redis_db.hdel('missions', missionId)
    #     return "Ok", 200
    # else:
    #     return "not found", 404

@device_blueprint.route("<string:deviceName>/join/<string:unitName>", methods=["POST"])
def joinUnit(deviceName, unitName):
    query = None
    # query = g.user and orm.checkPermission(g.user.name, groupName)

    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # if g.user and (g.user.role >= 50 or (query and query.role == 2)):
    try:
        if redis.findDevice(deviceName) and redis.findUnit(unitName):
            redis.joinUnit(unitName, deviceName)
            return ("Ok", 200)
        else:
            return("Object not founds.", 404)
    except Exception as e:
        return (e.__str__()+"\nMost likely duplicate.", 400)
    # else:
    #     return ("Unauthorized", 403)


@device_blueprint.route("<string:deviceName>/leave/<string:unitName>", methods=["POST"])
def leaveUnit(deviceName, unitName):
    query = None
    # query = g.user and orm.checkPermission(g.user.name, groupName)
    # app.logger.info(g.user.role)
    # return ("ok",200)


    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # if g.user and (g.user.role >= 50 or (query and query.role == 2)):
    try:
        return redis.leaveUnit(unitName, deviceName)
    except Exception as e:
        return(e.__str__()+"\nMost likely object not found.", 400)
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # else:
    #     return ("Unauthorized", 403)