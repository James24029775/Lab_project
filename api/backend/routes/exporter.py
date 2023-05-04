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
            # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
            # listDevices()不是原本的(是用listAllDevices())，之後要改回第一年的listDevices()的做法
            for membership in redis.listDevices(unit['unitId']):
                deviceName = redis.findDeviceById(membership['deviceId'])
                deviceId = membership['deviceId']

                # check if device online
                # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                keys = set()
                # for key in redis.db.keys():
                #     if "_" in key.decode():
                #         keys.add(key.decode().split("_")[1])

                # 在這裡打住，因為要先釐清heartbeat怎麼運作，不然根本沒有下面那些資料可以展示！！！！！！！！！！！！！！！！！！！！！！！
                # 但好像又沒差，因為txbitrate, rssi可以是N/A
                if deviceName in keys:
                    # online     
                    device = {
                            "deviceId":membership['deviceId'],
                            "name": membership['deviceName'],
                            "secret": membership['secret'],
                            # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                            # "ip": redis.db["ip_%s" % device.name].decode(),
                            # "txbitrate": redis.db["txbitrate_%s" % device.name].decode(),
                            # "rssi": redis.db["rssi_%s" % device.name].decode(),
                            "ip": 'None',
                            "txbitrate": 'None',
                            "rssi": 'None',
                            "status": True
                        }
                else:
                    # offline
                    device = {
                            "deviceId":membership['deviceId'],
                            "name": membership['deviceName'],
                            "secret": membership['secret'],
                            "ip": membership['ip'],
                            "txbitrate": '',
                            "rssi": '',
                            "status": False
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
    app.logger.info(result)
    return (json.dumps(result), 200)
