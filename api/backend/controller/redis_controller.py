import redis
import json
import time
import uuid
import _thread
from main import g, app

class device:
    @staticmethod
    def add(deviceName, secret, ip, redis_db, timestamp):
        deviceId = str(uuid.uuid4())
        # 將任務資料設定到 Redis 中
        deviceData = {
            'deviceName': deviceName,
            'secret': secret,
            'ip': ip,
            'timestamp': timestamp,
        }
        device_data_str = json.dumps(deviceData)
        redis_db.hmset('devices', {deviceId: device_data_str})

    @staticmethod
    def getIdByName(queryDeviceName, redis_db):
        devices = redis_db.hgetall('devices')
        for deviceId, deviceData in devices.items():
            deviceId = deviceId.decode('utf-8') # 將 bytes 轉換為字串
            deviceData = json.loads(deviceData.decode('utf-8'))
            deviceName = deviceData['deviceName']

            if deviceName == queryDeviceName:
                return deviceId
            
        return None

    @staticmethod
    def getNameById(queryDeviceId, redis_db):
        devices = redis_db.hgetall('devices')
        for deviceId, deviceData in devices.items():
            deviceId = deviceId.decode('utf-8') # 將 bytes 轉換為字串
            deviceData = json.loads(deviceData.decode('utf-8'))
            deviceName = deviceData['deviceName']

            if deviceId == queryDeviceId:
                return deviceName
            
        return None
    
    @staticmethod
    def get_all(redis_db):
        result = []
        devices = redis_db.hgetall('devices')
        for deviceId, deviceData in devices.items():
            deviceId = deviceId.decode('utf-8') # 將 bytes 轉換為字串
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
        groupId = str(uuid.uuid4())
        # 將任務資料設定到 Redis 中
        groupData = {
            'groupName': groupName
        }
        group_data_str = json.dumps(groupData)
        redis_db.hmset('groups', {groupId: group_data_str})

    @staticmethod
    def getIdByName(queryGroupName, redis_db):
        groups = redis_db.hgetall('groups')
        for groupId, groupData in groups.items():
            groupId = groupId.decode('utf-8') # 將 bytes 轉換為字串
            groupData = json.loads(groupData.decode('utf-8'))
            groupName = groupData['groupName']

            if groupName == queryGroupName:
                return groupId
            
        return None

    @staticmethod
    def get_all(redis_db):
        result = []
        groups = redis_db.hgetall('groups')
        for groupId, groupData in groups.items():
            groupId = groupId.decode('utf-8') # 將 bytes 轉換為字串
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
        unitId = str(uuid.uuid4())
        # 將任務資料設定到 Redis 中
        unitData = {
            'unitName': unitName,
            'groupId': groupId,
            'bandwidthLimit': bandwidthLimit,
        }
        unit_data_str = json.dumps(unitData)
        redis_db.hmset('units', {unitId: unit_data_str})

    @staticmethod
    def get_all(groupId, redis_db):
        result = []
        units = redis_db.hgetall('units')
        for unitId, unitData in units.items():
            unitId = unitId.decode('utf-8') # 將 bytes 轉換為字串
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
    
    @staticmethod
    def getIdByName(queryUnitName, redis_db):
        units = redis_db.hgetall('units')
        for unitId, unitData in units.items():
            unitId = unitId.decode('utf-8') # 將 bytes 轉換為字串
            unitData = json.loads(unitData.decode('utf-8'))
            unitName = unitData['unitName']

            if unitName == queryUnitName:
                return unitId
            
        return None


class membership:
    @staticmethod
    def add_membership(uid, did, redis_db):
        key = f'membership:{uid}'
        value = {did: 1}
        redis_db.hset(key, mapping=value)

    @staticmethod
    def delete_membership(uid, did, redis_db):
        key = f'membership:{uid}'
        redis_db.hdel(key, did)

    @staticmethod
    def get_devices_by_unit(uid, redis_db):
        key = f'membership:{uid}'
        return list(map(int, redis_db.hkeys(key)))


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
        

# class membership(db.Model):
#     __tablename__   = "membership"
#     __table_args__ = (db.UniqueConstraint("unitId", "deviceId"), db.PrimaryKeyConstraint("unitId", "deviceId"))

#     unitId = db.Column(db.Integer, db.ForeignKey("units.unitId"), nullable = False)
#     deviceId  = db.Column(db.Integer, db.ForeignKey("devices.deviceId"), nullable = False)

#     def __init__(self, uid, did):
#         self.unitId = uid
#         self.deviceId = did

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
        return group.get_all(self.redis_db)
    
    def addGroup(self, groupName):
        group.add(groupName, self.redis_db)

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

    def findGroup(self, groupName):
        result = group.getIdByName(groupName, self.redis_db)
        return result
    
    # def delGroup(self, groupName):
    #     db.session.delete(self.findGroup(groupName))
    #     db.session.commit()


    ########################################About Units###############################################
    def listUnits(self, groupId):
        result = unit.get_all(groupId, self.redis_db)
        return result
    
    def addUnit(self, groupName, unitName, bandwidthLimit):
        groupId = group.getIdByName(groupName, self.redis_db)
        if groupId is None:
            raise ValueError
        else:
            unit.add(unitName, groupId, bandwidthLimit, self.redis_db)

    def findUnit(self, unitName):
        unitId = unit.getIdByName(unitName, self.redis_db)
        return unitId

    # def joinUnit(self, unitName, deviceName):
    #     unitId = self.findUnit(unitName).unitId
    #     deviceId = self.findDevice(deviceName).deviceId
    #     db.session.add(membership(unitId, deviceId));
    #     db.session.commit()

    # def leaveUnit(self, unitName, deviceName):
    #     unitId = self.findUnit(unitName).unitId
    #     deviceId = self.findDevice(deviceName).deviceId
    #     db.session.delete(membership.query.filter_by(unitId = unitId, deviceId = deviceId).first())
    #     db.session.commit()

    

    ########################################About Devices###############################################
    def addDevice(self, deviceName, secret, ip, timestamp):
        device.add(deviceName, secret, ip, timestamp, self.redis_db)

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
        # result= membership.query.filter_by(unitId = uid)
        # return result
        return self.listAllDevices()

    def listAllDevices(self):
        result = device.get_all(self.redis_db)
        return result
    
    # def delDevice(self, deviceName):
    #     db.session.delete(self.findDevice(deviceName))
    #     db.session.commit()