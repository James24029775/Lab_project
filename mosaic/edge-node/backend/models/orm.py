from main import db
import jwt
import bcrypt
from datetime import timezone, datetime
from main import db

class device(db.Model):
    __tablename__ = 'devices'

    deviceId  = db.Column(db.Integer, nullable = False, 
                        primary_key = True, autoincrement=True)
    name    = db.Column(db.String(256), nullable = False, unique = True)
    secret  = db.Column(db.String(256), nullable = False)
    ip      = db.Column(db.String(16), nullable = False)

    def __init__(self, name, secret, ip):
        self.name   = name
        self.secret = secret
        self.ip     = ip

class user(db.Model):
    __tablename__ = 'users'

    userId  = db.Column(db.Integer, nullable = False, 
                        primary_key = True, autoincrement = True)
    name     = db.Column(db.String(256), nullable = False, unique = True)
    password = db.Column(db.String(128), nullable = False)
    role  = db.Column(db.Integer, nullable=False, default = 0)

    def __init__(self, name, pwd, adm):
        self.name = name
        self.password = pwd
        self.role = adm

    def jwt(self, secret):

        now = int(datetime.now(tz=timezone.utc).timestamp())
        token = {}
        token['iss'] = 'owo.owo'
        token['exp'] = (now) + 3600
        token['iat'] = token['nbf'] = now

        token['userName'] = self.name

        return jwt.encode(token, secret, algorithm="HS256")

    def login(self, plain, secret):
        if self.password == "" or bcrypt.checkpw(plain.encode(), self.password.encode()):
            return self.jwt(secret)
        return None
    
    def passwd(self, plain, secret):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(plain.encode(), salt)
        db.session.commit()
        
    def setRole(self, role):
        self.role = role
        db.session.commit()

class group(db.Model):
    __tablename__ = 'groups'

    groupId  = db.Column(db.Integer, nullable = False,
                         primary_key = True, autoincrement = True)
    name     = db.Column(db.String(32), nullable = False, unique = True)

    def __init__(self, name):
        self.name = name  

class groupDevice(db.Model):
    __tablename__ = "groupDevices"
    __table_args__ = (db.UniqueConstraint("groupId", "deviceId"), db.PrimaryKeyConstraint("groupId", "deviceId"))
    
    groupId = db.Column(db.Integer, db.ForeignKey("groups.groupId"), nullable = False)
    deviceId  = db.Column(db.Integer, db.ForeignKey("devices.deviceId"), nullable = False)

    def __init__(self, gid, did):
        self.groupId = gid
        self.deviceId = did

class groupPermission(db.Model):
    __tablename__   = "groupPermissions"
    __table_args__ = (db.UniqueConstraint("groupId", "userId"), db.PrimaryKeyConstraint("groupId", "userId"))

    groupId = db.Column(db.Integer, db.ForeignKey("groups.groupId"), nullable = False)
    userId  = db.Column(db.Integer, db.ForeignKey("users.userId"), nullable = False)
    role    = db.Column(db.Integer, nullable = False)

    def __init__(self, gid, uid, role):
        self.groupId = gid
        self.userId = uid
        self.role = role
        # 0 -> None
        # 1 -> RO
        # 2 -> RW
        
class unit(db.Model):
    __tablename__   = "units"

    unitId  = db.Column(db.Integer, nullable = False,
                       primary_key = True, autoincrement = True)
    name    = db.Column(db.String(32), nullable = False, unique = True)
    groupId = db.Column(db.Integer, db.ForeignKey("groups.groupId"), nullable = False) 
    bandwidthLimit    = db.Column(db.String(32), nullable = True)

    def __init__(self, name, gid, bandwidthLimit):
        self.name = name
        self.groupId = gid
        self.bandwidthLimit = bandwidthLimit

class membership(db.Model):
    __tablename__   = "membership"
    __table_args__ = (db.UniqueConstraint("unitId", "deviceId"), db.PrimaryKeyConstraint("unitId", "deviceId"))

    unitId = db.Column(db.Integer, db.ForeignKey("units.unitId"), nullable = False)
    deviceId  = db.Column(db.Integer, db.ForeignKey("devices.deviceId"), nullable = False)

    def __init__(self, uid, did):
        self.unitId = uid
        self.deviceId = did

class policies(db.Model):
    __tablename__   = "policies"

    policyId  = db.Column(db.Integer, nullable = False,
                       primary_key = True, autoincrement = True)
    source = db.Column(db.Integer, nullable = False)
    destination  = db.Column(db.Integer, nullable = False)
    limits  = db.Column(db.Integer, nullable = False)

    def __init__(self, src, dst, lim):
        self.source = src
        self.destination = dst
        self.limits = lim

class database():
    def __init__(self, logger):
        self.logger = logger 

    def addDevice(self, deviceName, secret, ip):
        db.session.add(device(deviceName, secret,ip))
        db.session.commit()

        
    def addUser(self, username, password, isAdmin):
        db.session.add(user(username, password, isAdmin))
        db.session.commit()
    
    def addGroup(self, groupName):
        db.session.add(group(groupName))
        db.session.commit()
    
    def addUnit(self, groupName, unitName, bandwidthLimit):
        groupId = self.findGroup(groupName).groupId
        db.session.add(unit(unitName, groupId, bandwidthLimit))
        db.session.commit()

    def addDeviceToGroup(self, deviceName, groupName):
        groupId = self.findGroup(groupName).groupId
        deviceId = self.findDevice(deviceName).deviceId
        db.session.add(groupDevice(groupId, deviceId))
        db.session.commit()

    def joinUnit(self, unitName, deviceName):
        unitId = self.findUnit(unitName).unitId
        deviceId = self.findDevice(deviceName).deviceId
        db.session.add(membership(unitId, deviceId));
        db.session.commit()

    def addPolicy(self, src, dst, lim):
        src = self.findDevice(src).deviceId
        dst = self.findDevice(dst).deviceId
        db.session.add(policies(src, dst, lim))
        db.session.commit()

    def delPolicy(self, src, dst, lim):
        src = self.findDevice(src).deviceId
        dst = self.findDevice(dst).deviceId
        db.session.delete(policies.query.filter_by(source = src, destination = dst, limits = lim).first())
        db.session.commit()

    def leaveUnit(self, unitName, deviceName):
        unitId = self.findUnit(unitName).unitId
        deviceId = self.findDevice(deviceName).deviceId
        db.session.delete(membership.query.filter_by(unitId = unitId, deviceId = deviceId).first())
        db.session.commit()

    def removeDeviceFromGroup(self, deviceName, groupName):
        groupId = self.findGroup(groupName).groupId
        deviceId = self.findDevice(deviceName).deviceId
        db.session.delete(groupDevice.query.filter_by(groupId = groupId, deviceId=deviceId).first())
        db.session.commit()
    
    def grantPermission(self, userName, groupName, newRole):
        result = self.checkPermission(userName, groupName)
        if result:
            result.role = newRole
        else:
            userId = self.findUser(userName).userId
            groupId = self.findGroup(groupName).groupId
            db.session.add(groupPermission(groupId, userId, newRole))
            db.session.commit()

    def checkPermission(self, userName, groupName):
        userId = self.findUser(userName).userId
        groupId = self.findGroup(groupName).groupId
        result = groupPermission.query.filter_by(groupId = groupId, userId = userId).first()
        return result
    
    def findDevice(self, deviceName):
        result = device.query.filter_by(name = deviceName).first()
        return result
    
    def findDeviceById(self, did):
        result = device.query.filter_by(deviceId = did).first()
        return result

    def findUser(self, userName):
        result = user.query.filter_by(name = userName).first()
        return result
    
    def findUnit(self, unitName):
        result = unit.query.filter_by(name = unitName).first()
        return result

    def listUsers(self, queryRole):
        result = user.query.filter_by(role < queryRole)
        return result

    def listGroups(self):
        result = group.query
        return result

    def listPolicies(self):
        return policies.query

    def listUnits(self, groupId):
        result = unit.query.filter_by(groupId = groupId);
        return result;

    def listDevices(self, uid):
        result= membership.query.filter_by(unitId = uid);
        return result

    def listAllDevices(self):
        result= device.query
        return result

    def findGroup(self, groupName):
        result = group.query.filter_by(name = groupName).first()
        return result
    
    def delDevice(self, deviceName):
        db.session.delete(self.findDevice(deviceName))
        db.session.commit()

    def delUnit(self, unitName):
        db.session.delete(self.findUnit(unitName))
        db.session.commit()

    def delUser(self, userName):
        db.session.delete(self.findUser(userName))
        db.session.commit()

    def delGroup(self, groupName):
        db.session.delete(self.findGroup(groupName))
        db.session.commit()
