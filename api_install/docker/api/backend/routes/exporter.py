from flask import Blueprint, request
from main import g, app, redis
import json

exporter_blueprint = Blueprint('exporter', __name__)

@exporter_blueprint.route("/", methods=["GET"])
def getUnits():
    result = []
    for group in redis.listGroups():
        # group_result = []
        for unit in redis.listUnits(group['groupId']):
            members = []
            for device in redis.listDevices(unit['unitId']):
                deviceName = redis.findDeviceById(device['deviceId'])

                # check if device online
                # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                keys = set()
                # for key in redis.db.keys():
                #     if "_" in key.decode():
                #         keys.add(key.decode().split("_")[1])

                # 在這裡打住，因為要先釐清heartbeat怎麼運作，不然根本沒有下面那些資料可以展示！！！！！！！！！！！！！！！！！！！！！！！
                # 但好像又沒差，因為txbitrate, rssi可以是N/A
                txbitrate = rssi = ssid = bssid = 'N/A'
                if deviceName in keys:
                    # online     
                    device = {
                        "deviceId":device['deviceId'],
                        "name": device['deviceName'],
                        "secret": device['secret'],
                        "ip": device['ip'],
                        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                        "txbitrate": txbitrate,
                        "rssi": rssi,
                        'ssid': ssid,
                        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                        'bssid': bssid,
                        'status': True,
                        'timestamp': device['timestamp'],
                        # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                        # "ip": redis.db["ip_%s" % device.name].decode(),
                        # "txbitrate": redis.db["txbitrate_%s" % device.name].decode(),
                        # "rssi": redis.db["rssi_%s" % device.name].decode(),
                    }
                else:
                    # offline
                    device = {
                        "name": device['deviceName'],
                        "secret": device['secret'],
                        "ip": device['ip'],
                        "txbitrate": txbitrate,
                        "rssi": rssi,
                        'ssid': ssid,
                        'bssid': bssid,
                        'status': False,
                        'timestamp': device['timestamp'],
                }
                members.append(device)
            unit_dir = {"unitId": unit['unitId'], "unitName": unit['unitName'], "bandwidthLimit": unit['bandwidthLimit'], "members": members}

            # unit_dir = {"unitId": unit.unitId, "unitName": unit.name, "members": members}
            result.append(unit_dir)
        #     group_result.append(unit_dir)
        # result.append(group_result)
    
    result = {"units": result}
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    # policies = []
    # for policy in orm.listPolicies():
    #     policies.append((policy.source, policy.destination, policy.limits))

    # result['policies'] = policies
    
    # app.logger.info(result)
    return (json.dumps(result), 200)
