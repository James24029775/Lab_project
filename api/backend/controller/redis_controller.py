import redis
import json
import time
import uuid
import _thread
from main import g, app

def prink(msg):
    print("\033[38;5;218m" + msg + "\033[0m")

class device:
    @staticmethod
    def add(deviceName, secret, ip, txbitrate, rssi, ssid, bssid, status, timestamp, redis_db):
        try:
            deviceId = str(uuid.uuid4())
            deviceData = {
                'deviceName': deviceName,
                'secret': secret,
                'ip': ip,
                'txbitrate': txbitrate,
                'rssi': rssi,
                'ssid': ssid,
                'bssid': bssid,
                'status': status,
                'timestamp': timestamp,
            }
            device_data_str = json.dumps(deviceData)
            redis_db.hmset('devices', {deviceId: device_data_str})
            prink('device:' + deviceName + ' add successfully.')
            return ("Ok", 200)

        except:
            prink('device:' + deviceName + ' failed to add.')
            return ("Bad request", 400)

    @staticmethod
    def delete(deviceName, redis_db):
        deviceId = device.getIdByName(deviceName, redis_db)
        try:
            redis_db.hdel('devices', deviceId)
            prink('device:' + deviceName + ' has been deleted.')
            try:
                uids = membership.getUnitIdByDeviceId(deviceId, redis_db)
                if len(uids) == 0:
                    prink('device:' + deviceName + ' does not have any membership.')
                    return ("Ok", 200)
                for uid in uids:
                    membership.delete(uid, deviceId, redis_db)
                prink('Membership about device:' + deviceName + ' has been deleted.')
                return ("Ok", 200)
            
            except:
                prink('Membership fail to delete.')
                return ("not found", 404)
        except:
            prink('device:' + deviceName + ' does not exist.')
            return ("not found", 404)

    @staticmethod
    def getIdByName(queryDeviceName, redis_db):
        devices = redis_db.hgetall('devices')
        for deviceId, deviceData in devices.items():
            deviceId = deviceId.decode('utf-8')
            deviceData = json.loads(deviceData.decode('utf-8'))
            deviceName = deviceData['deviceName']

            if deviceName == queryDeviceName:
                return deviceId
            
        return None

    @staticmethod
    def getNameById(queryDeviceId, redis_db):
        devices = redis_db.hgetall('devices')
        for deviceId, deviceData in devices.items():
            deviceId = deviceId.decode('utf-8')
            deviceData = json.loads(deviceData.decode('utf-8'))
            deviceName = deviceData['deviceName']

            if deviceId == queryDeviceId:
                return deviceName
            
        return None
    
    @staticmethod
    def getAll(redis_db):
        result = []
        devices = redis_db.hgetall('devices')
        for deviceId, deviceData in devices.items():
            deviceId = deviceId.decode('utf-8')
            deviceData = json.loads(deviceData.decode('utf-8')) 
            device = {
                'deviceId': deviceId,
                'deviceName': deviceData.get('deviceName', ''),
                'secret': deviceData.get('secret', ''),
                'ip': deviceData.get('ip', ''),
                'txbitrate': deviceData.get('txbitrate', ''),
                'rssi': deviceData.get('rssi', ''),
                'ssid': deviceData.get('ssid', ''),
                'bssid': deviceData.get('bssid', ''),
                'status': deviceData.get('status', ''),
                'timestamp': deviceData.get('timestamp', ''),
            }
            result.append(device)

        return result

# class user(db.Model):
#     __tablename__ = 'users'

#     userId  = db.Column(db.Integer, nullable = False, 
#                         primary_key = True, autoincrement = True)
#     name     = db.Column(db.String(256), nullable = False, unique = True)
#     password = db.Column(db.String(128), nullable = False)
#     role  = db.Column(db.Integer, nullable=False, default = 0)

#     def __init__(self, name, pwd, adm):
#         self.name = name
#         self.password = pwd
#         self.role = adm

#     def jwt(self, secret):

#         now = int(datetime.now(tz=timezone.utc).timestamp())
#         token = {}
#         token['iss'] = 'owo.owo'
#         token['exp'] = (now) + 3600
#         token['iat'] = token['nbf'] = now

#         token['userName'] = self.name

#         return jwt.encode(token, secret, algorithm="HS256")

#     def login(self, plain, secret):
#         if self.password == "" or bcrypt.checkpw(plain.encode(), self.password.encode()):
#             return self.jwt(secret)
#         return None
    
#     def passwd(self, plain, secret):
#         salt = bcrypt.gensalt()
#         self.password = bcrypt.hashpw(plain.encode(), salt)
#         db.session.commit()
        
#     def setRole(self, role):
#         self.role = role
#         db.session.commit()

class group:
    @staticmethod
    def add(groupName, redis_db):
        try:
            groupId = str(uuid.uuid4())
            groupData = {
                'groupName': groupName
            }
            group_data_str = json.dumps(groupData)
            redis_db.hmset('groups', {groupId: group_data_str})
            prink('group:' + groupName + ' add successfully.')
            return ("Ok", 200)

        except:
            prink('group:' + groupName + ' failed to add.')
            return ("not found", 404)
        
    # @staticmethod
    # def delete(groupName, redis_db):

    @staticmethod
    def getIdByName(queryGroupName, redis_db):
        groups = redis_db.hgetall('groups')
        for groupId, groupData in groups.items():
            groupId = groupId.decode('utf-8')
            groupData = json.loads(groupData.decode('utf-8'))
            groupName = groupData['groupName']

            if groupName == queryGroupName:
                return groupId
            
        return None

    @staticmethod
    def getAll(redis_db):
        result = []
        groups = redis_db.hgetall('groups')
        for groupId, groupData in groups.items():
            groupId = groupId.decode('utf-8')
            groupData = json.loads(groupData.decode('utf-8')) 
            group = {
                'groupId': groupId,
                'groupName': groupData.get('groupName', ''),
            }
            result.append(group)

        return result


class unit:
    @staticmethod
    def add(unitName, groupId, bandwidthLimit, redis_db):
        try:
            unitId = str(uuid.uuid4())
            unitData = {
                'unitName': unitName,
                'groupId': groupId,
                'bandwidthLimit': bandwidthLimit,
            }
            unit_data_str = json.dumps(unitData)
            redis_db.hmset('units', {unitId: unit_data_str})
            prink('unit:' + unitName + ' add successfully.')
            return ("Ok", 200)
        
        except:
            prink('unit:' + unitName + ' failed to add.')
            return ("Bad request", 400)
        
    @staticmethod
    def delete(queryUnitName, redis_db):
        unitId = unit.getIdByName(queryUnitName, redis_db)
        try:
            redis_db.hdel('units', unitId)
            prink('unit:' + queryUnitName + ' has been deleted.')
            try:
                devices = membership.getDevicesByUnitId(unitId, redis_db)
                if len(devices) == 0:
                    prink('unit:' + queryUnitName + ' does not have any membership.')
                    return ("Ok", 200)
                
                for device in devices:
                    deviceId = device['deviceId']
                    deviceName = device['deviceName']
                    membership.delete(unitId, deviceId, redis_db)
                return ("Ok", 200)
                
            except:
                prink('Membership of ' + queryUnitName + ' and ' + deviceName + ' does not exist.')
                return ("not found", 404)

        except:
            prink('Membership fail to delete.')
            return ("not found", 404)
    
    @staticmethod
    def getIdByName(queryUnitName, redis_db):
        units = redis_db.hgetall('units')
        for unitId, unitData in units.items():
            unitId = unitId.decode('utf-8')
            unitData = json.loads(unitData.decode('utf-8'))
            unitName = unitData['unitName']

            if unitName == queryUnitName:
                return unitId
            
        return None
    
    @staticmethod
    def getNameById(queryUnitId, redis_db):
        units = redis_db.hgetall('units')
        for unitId, unitData in units.items():
            unitId = unitId.decode('utf-8')
            unitData = json.loads(unitData.decode('utf-8'))
            unitName = unitData['unitName']

            if unitId == queryUnitId:
                return unitName
            
        return None

    @staticmethod
    def getAll(groupId, redis_db):
        result = []
        units = redis_db.hgetall('units')
        for unitId, unitData in units.items():
            unitId = unitId.decode('utf-8')
            unitData = json.loads(unitData.decode('utf-8')) 
            unit = {
                'unitId': unitId,
                'unitName': unitData.get('unitName', ''),
                'groupId': unitData.get('groupId', ''),
                'bandwidthLimit': unitData.get('bandwidthLimit', ''),
            }
            if unit['groupId'] == groupId:
                result.append(unit)

        return result


class membership:
    @staticmethod
    def add(uid, did, redis_db):
        try:
            unitName = unit.getNameById(uid, redis_db)
            deviceName = device.getNameById(did, redis_db)
            value = unitName + ':' + deviceName
            key = str(uid) + ':' + str(did)
            redis_db.hset("membership", key, value)
            prink('membership:' + value + ' add successfully.')
            return ("Ok", 200)
        except:
            prink('membership:' + value + ' failed to add.')
            return ("Bad request", 400)

    @staticmethod
    def delete(uid, did, redis_db):
        try:
            key = str(uid) + ':' + str(did)
            value = redis_db.hget("membership", key).decode('utf-8')
            if value is None:
                prink('membership does not exist.')
                return ("not found", 404)
            else:
                redis_db.hdel("membership", key)
                prink('membership:' + value + ' delete successfully')
                return ('Ok', 200)
        except:
            prink('membership:' + value + ' failed to delete.')
            return ("not found", 404)

    @staticmethod
    def getDevicesByUnitId(queryUid, redis_db):
        memberships = redis_db.hgetall("membership")
        result = []
        for key, value in memberships.items():
            key = key.decode('utf-8')
            key = key.split(':')
            uid, did = key[0], key[1]
            if uid == queryUid:
                deviceData = redis_db.hget('devices', did)
                deviceData = json.loads(deviceData.decode('utf-8')) 
                device = {
                    'deviceId': did,
                    'deviceName': deviceData.get('deviceName', ''),
                    'secret': deviceData.get('secret', ''),
                    'ip': deviceData.get('ip', ''),
                    'txbitrate': deviceData.get('txbitrate', ''),
                    'rssi': deviceData.get('rssi', ''),
                    'ssid': deviceData.get('ssid', ''),
                    'bssid': deviceData.get('bssid', ''),
                    'status': deviceData.get('status', ''),
                    'timestamp': deviceData.get('timestamp', ''),
                }
                result.append(device)
            
        return result

    @staticmethod
    def getUnitIdByDeviceId(queryDid, redis_db):
        memberships = redis_db.hgetall("membership")
        result = []
        for key, value in memberships.items():
            key = key.decode('utf-8')
            key = key.split(':')
            uid, did = key[0], key[1]
            if did == queryDid:
                result.append(uid)
            
        return result

# class groupDevice(db.Model):
#     __tablename__ = "groupDevices"
#     __table_args__ = (db.UniqueConstraint("groupId", "deviceId"), db.PrimaryKeyConstraint("groupId", "deviceId"))
    
#     groupId = db.Column(db.Integer, db.ForeignKey("groups.groupId"), nullable = False)
#     deviceId  = db.Column(db.Integer, db.ForeignKey("devices.deviceId"), nullable = False)

#     def __init__(self, gid, did):
#         self.groupId = gid
#         self.deviceId = did

# class groupPermission(db.Model):
#     __tablename__   = "groupPermissions"
#     __table_args__ = (db.UniqueConstraint("groupId", "userId"), db.PrimaryKeyConstraint("groupId", "userId"))

#     groupId = db.Column(db.Integer, db.ForeignKey("groups.groupId"), nullable = False)
#     userId  = db.Column(db.Integer, db.ForeignKey("users.userId"), nullable = False)
#     role    = db.Column(db.Integer, nullable = False)

#     def __init__(self, gid, uid, role):
#         self.groupId = gid
#         self.userId = uid
#         self.role = role
#         # 0 -> None
#         # 1 -> RO
#         # 2 -> RW


# class policies(db.Model):
#     __tablename__   = "policies"

#     policyId  = db.Column(db.Integer, nullable = False,
#                        primary_key = True, autoincrement = True)
#     source = db.Column(db.Integer, nullable = False)
#     destination  = db.Column(db.Integer, nullable = False)
#     limits  = db.Column(db.Integer, nullable = False)

#     def __init__(self, src, dst, lim):
#         self.source = src
#         self.destination = dst
#         self.limits = lim

class redis_controller:
    def __init__(self, logger, callback):
        self.redis_db = redis.StrictRedis(host = "127.0.0.1", port = 6379, db = 0)
        self.logger = logger
        _thread.start_new_thread(self.timeout_check, (callback, ))

    def timeout_check(self, callback):
        while True:
            for x in self.redis_db.zpopmin("timer"):
                deviceId, expireTime = x
                deviceId = deviceId.decode()
                
                deviceTimeout = lambda: float(self.redis_db["timer_%s" % deviceId].decode())
                while time.time() <= expireTime:
                    time.sleep(1)

                self.logger.info(deviceTimeout())
                if expireTime < deviceTimeout():    
                    self.redis_db.zadd("timer", {deviceId: deviceTimeout()})
                    continue
                callback(deviceId)
                self.redis_db.delete("timer_%s" % deviceId)
                self.redis_db.delete("ip_%s" % deviceId)
                self.redis_db.delete("secret_%s" % deviceId)
                self.redis_db.delete("txbitrate_%s" % deviceId)
                self.redis_db.delete("rssi_%s" % deviceId)
                self.redis_db.delete("ssid_%s" % deviceId)
                self.redis_db.delete("bssid_%s" % deviceId)
            
    def add_timer(self, deviceId, ip, secret, txbitrate, rssi, ssid, bssid):
        now =time.time()
        self.redis_db.zadd("timer", {deviceId: now + 10})
        self.redis_db["timer_%s" % deviceId] = now + 10
        self.redis_db["ip_%s" % deviceId] = ip
        self.redis_db["secret_%s" % deviceId] = secret
        self.redis_db["txbitrate_%s" % deviceId] = txbitrate
        self.redis_db["rssi_%s" % deviceId] = rssi
        self.redis_db["ssid_%s" % deviceId] = ssid
        self.redis_db["bssid_%s" % deviceId] = bssid

    ########################################About Groups###############################################
    def listGroups(self):
        return group.getAll(self.redis_db)
    
    def addGroup(self, groupName):
        return group.add(groupName, self.redis_db)

    # def addDeviceToGroup(self, deviceName, groupName):
    #     groupId = self.findGroup(groupName).groupId
    #     deviceId = self.findDevice(deviceName).deviceId
    #     db.session.add(groupDevice(groupId, deviceId))
    #     db.session.commit()

    # def removeDeviceFromGroup(self, deviceName, groupName):
    #     groupId = self.findGroup(groupName).groupId
    #     deviceId = self.findDevice(deviceName).deviceId
    #     db.session.delete(groupDevice.query.filter_by(groupId = groupId, deviceId=deviceId).first())
    #     db.session.commit()

    # def findGroup(self, groupName):
    #     result = group.getIdByName(groupName, self.redis_db)
    #     return result
    
    # def delGroup(self, groupName):
    #     db.session.delete(self.findGroup(groupName))
    #     db.session.commit()


    ########################################About Units###############################################
    def listUnits(self, groupId):
        result = unit.getAll(groupId, self.redis_db)
        return result
    
    def addUnit(self, groupName, unitName, bandwidthLimit):
        groupId = group.getIdByName(groupName, self.redis_db)
        if groupId is None:
            prink('group:' + groupName + ' does not exist.')
            return ("Bad request", 400)
        else:
            return unit.add(unitName, groupId, bandwidthLimit, self.redis_db)

    def findUnit(self, unitName):
        unitId = unit.getIdByName(unitName, self.redis_db)
        return unitId

    def joinUnit(self, unitName, deviceName):
        unitId = unit.getIdByName(unitName, self.redis_db)
        deviceId = device.getIdByName(deviceName, self.redis_db)
        membership.add(unitId, deviceId, self.redis_db)

    def leaveUnit(self, unitName, deviceName):
        unitId = unit.getIdByName(unitName, self.redis_db)
        deviceId = device.getIdByName(deviceName, self.redis_db)
        if unitId is None:
            prink('unit:' + unitName + ' does not exist.')
            return ('Object not founds', 400)
        if deviceId is None:
            prink('device:' + deviceName + ' does not exist.')
            return ('Object not founds', 400)
        return membership.delete(unitId, deviceId, self.redis_db)

    def delUnit(self, unitName):
        return unit.delete(unitName, self.redis_db)

    ########################################About Devices###############################################
    def addDevice(self, deviceName, secret, ip, txbitrate, rssi, ssid, bssid, status, timestamp):
        return device.add(deviceName, secret, ip, txbitrate, rssi, ssid, bssid, status, timestamp, self.redis_db)
    
    def delDevice(self, deviceName):
        return device.delete(deviceName, self.redis_db)

    # def addDeviceToGroup(self, deviceName, groupName):
    #     groupId = self.findGroup(groupName).groupId
    #     deviceId = self.findDevice(deviceName).deviceId
    #     db.session.add(groupDevice(groupId, deviceId))
    #     db.session.commit()

    # def removeDeviceFromGroup(self, deviceName, groupName):
    #     groupId = self.findGroup(groupName).groupId
    #     deviceId = self.findDevice(deviceName).deviceId
    #     db.session.delete(groupDevice.query.filter_by(groupId = groupId, deviceId=deviceId).first())
    #     db.session.commit()
    
    def findDevice(self, deviceName):
        return device.getIdByName(deviceName, self.redis_db)
    
    def findDeviceById(self, did):
        return device.getNameById(did, self.redis_db)

    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    def listDevices(self, unitId):
        return membership.getDevicesByUnitId(unitId, self.redis_db)

    def listAllDevices(self):
        return device.getAll(self.redis_db)
    
