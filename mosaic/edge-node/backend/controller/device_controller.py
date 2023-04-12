# def check(func):
#     try:
#         def wrap(self, *args, **kwargs):
#             res = func(self, *args, **kwargs)
#             return res
#     except Exception as e:
#         self.logger.warning(e.__str__())
#     return


class device_controller:
    
    def __init__(self, appLogger, db):
        self.logger = appLogger
        self.db = db

    def addDevice(self, name, secret, ip):
        self.db.addDevice(name, secret, ip)

    # @check
    def addGroup(self, groupName):
        # try:
            self.db.addGroup(groupName)
        # except Exception as e:
        #     self.logger.info(e.__str__);
    def findDevice(self, name):
        return self.db.findDevice(name)
    
    def addDeviceToGroup(self, devicename, groupname):
        self.db.addDeviceToGroup(devicename, groupname)

    def removeDeviceFromGroup(self, devicename, groupname):
        self.db.removeDeviceFromGroup(devicename, groupname)

    def grantPermission(self, user, group, role):
        self.db.grantPermission(user, group, role)

    def authorize(self, user, group):
        result = self.db.checkPermission(user, group)
        if result:
            return result.role
        return 0
