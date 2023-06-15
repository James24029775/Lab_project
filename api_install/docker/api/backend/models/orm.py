from main import db
import jwt
import bcrypt
from datetime import timezone, datetime

class mission(db.Model):
    __tablename__ = 'missions'

    missionId  = db.Column(db.Integer, nullable = False, 
                        primary_key = True, autoincrement=True)
    name    = db.Column(db.String(256), nullable = False, unique = True)
    secret  = db.Column(db.String(256), nullable = False)
    ip      = db.Column(db.String(16), nullable = False)

    def __init__(self, name, secret, ip):
        self.name   = name
        self.secret = secret
        self.ip     = ip


class database():
    def __init__(self, logger):
        self.logger = logger 

    def addDevice(self, deviceName, secret, ip):
        db.session.add(device(deviceName, secret,ip))
        db.session.commit()
    
    def findDevice(self, deviceName):
        result = device.query.filter_by(name = deviceName).first()
        return result
    
    def findDeviceById(self, did):
        result = device.query.filter_by(deviceId = did).first()
        return result

    # def listDevices(self, uid):
    #     result= membership.query.filter_by(unitId = uid);
    #     return result

    def listAllDevices(self):
        result= device.query
        return result
    
    def delDevice(self, deviceName):
        db.session.delete(self.findDevice(deviceName))
        db.session.commit()