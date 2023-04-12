from flask import Blueprint, request
from main import g, users, app, orm, redis
import json

exporter_blueprint = Blueprint('exporter', __name__)

@exporter_blueprint.route("/", methods=["GET"])
def getUnits():
    result = []
    for group in orm.listGroups():
        # group_result = []
        for unit in orm.listUnits(group.groupId):
            members = []
            for membership in orm.listDevices(unit.unitId):
                device = orm.findDeviceById(membership.deviceId)

                # check if device online
                keys = set()
                for key in redis.db.keys():
                    if "_" in key.decode():
                        keys.add(key.decode().split("_")[1])
                if device.name in keys:
                    # online     
                    device = {
                            "deviceId": device.deviceId,
                            "name": device.name,
                            "secret": device.secret,
                            "ip": redis.db["ip_%s" % device.name].decode(),
                            "txbitrate": redis.db["txbitrate_%s" % device.name].decode(),
                            "rssi": redis.db["rssi_%s" % device.name].decode(),
                            "status": True
                        }
                else:
                    # offline
                    device = {
                            "deviceId": device.deviceId,
                            "name": device.name,
                            "secret": device.secret,
                            "ip": device.ip,
                            "txbitrate": '',
                            "rssi": '',
                            "status": False
                        }
                members.append(device)
            unit_dir = {"unitId": unit.unitId, "unitName": unit.name, "bandwidthLimit": unit.bandwidthLimit, "members": members}

            # unit_dir = {"unitId": unit.unitId, "unitName": unit.name, "members": members}
            result.append(unit_dir)
        #     group_result.append(unit_dir)
        # result.append(group_result)
    
    result = {"units": result}
    policies = []
    for policy in orm.listPolicies():
        policies.append((policy.source, policy.destination, policy.limits))

    result['policies'] = policies
    app.logger.info(result)
    return (json.dumps(result), 200)
