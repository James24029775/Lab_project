import redis
import time
import _thread

class redis_controller:
    def __init__(self, logger, callback):
        self.db = redis.StrictRedis(host = "172.18.2.1", port = 6379, db = 0)
        self.logger = logger
        _thread.start_new_thread(self.timeout_check, (callback, ))

    def timeout_check(self, callback):
        while True:
            for x in self.db.zpopmin("timer"):
                deviceId, expireTime = x
                deviceId = deviceId.decode()
                
                deviceTimeout = lambda: float(self.db["timer_%s" % deviceId].decode())
                while time.time() <= expireTime:
                    time.sleep(1)

                self.logger.info(deviceTimeout())
                if expireTime < deviceTimeout():    
                    self.db.zadd("timer", {deviceId: deviceTimeout()})
                    continue
                callback(deviceId)
                self.db.delete("timer_%s" % deviceId)
                self.db.delete("ip_%s" % deviceId)
                self.db.delete("secret_%s" % deviceId)
                self.db.delete("txbitrate_%s" % deviceId)
                self.db.delete("rssi_%s" % deviceId)
                self.db.delete("ssid_%s" % deviceId)
                self.db.delete("bssid_%s" % deviceId)
            
    def add_timer(self, deviceId, ip, secret, txbitrate, rssi, ssid, bssid):
        now =time.time()
        self.db.zadd("timer", {deviceId: now + 10})
        self.db["timer_%s" % deviceId] = now + 10
        self.db["ip_%s" % deviceId] = ip
        self.db["secret_%s" % deviceId] = secret
        self.db["txbitrate_%s" % deviceId] = txbitrate
        self.db["rssi_%s" % deviceId] = rssi
        self.db["ssid_%s" % deviceId] = ssid
        self.db["bssid_%s" % deviceId] = bssid
