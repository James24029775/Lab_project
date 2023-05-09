import redis

# 建立 Redis 連線物件
r = redis.Redis(host='localhost', port=6379, db=0)

# 創建名為 membership 的 hash
r.hset("membership", "unitId:1:deviceId:2", "value")
r.hset("membership", "unitId:1:deviceId:2333", "value")

# 檢索 hash 中的所有資料
result = r.hgetall("membership")
result = r.hget("membership", )
print(result)
