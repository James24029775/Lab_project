from flask import Blueprint, request, jsonify
import time
import json
import uuid
from main import g, app, redis_db, conn

mission_blueprint = Blueprint('missionManager', __name__)

# 定義 API 路由
# 'mission' Redis API 的路由
@mission_blueprint.route('getmission', methods=['GET'])
def get_missions():
    # 從 Redis 取得任務資料
    missions = redis_db.hgetall('missions')

    # 轉換資料為所需的格式
    mission_list = []
    for missionId, mission_data in missions.items():
        missionId = missionId.decode('utf-8') # 將 bytes 轉換為字串
        mission_data = json.loads(mission_data.decode('utf-8')) 
        mission = {
            'missionId': missionId,
            'missionName': mission_data.get('missionName', ''),
            'MYSELF_Longitude': mission_data.get('MYSELF_Longitude', ''),
            'MYSELF_Latitude': mission_data.get('MYSELF_Latitude', ''),
            'time': mission_data.get('time', '')
        }
        mission_list.append(mission)
    mission_list.sort(key=lambda x: float(x['time']), reverse=True)
    return mission_list, 200


@mission_blueprint.route('fetch/<string:missionId>', methods=['GET'])
def get_missions_by_ID(missionId):
    mission_data = redis_db.hget("missions", missionId)
    mission_data = json.loads(mission_data.decode('utf-8')) 
    mission = {
        'missionId': missionId,
        'missionName': mission_data.get('missionName', ''),
        'MYSELF_Longitude': mission_data.get('MYSELF_Longitude', ''),
        'MYSELF_Latitude': mission_data.get('MYSELF_Latitude', '')
    }
    return mission, 200


@mission_blueprint.route('createmission', methods=['POST'])
def create_mission():
    # 取得前端傳遞的任務資料
    mission_name = request.get_json()['missionName']
    myself_longitude = request.get_json()['MYSELF_Longitude']
    myself_latitude = request.get_json()['MYSELF_Latitude']
    myself_timer = time.time()
    
    # 將任務資料設定到 Redis 中
    mission_data = {
        'missionName': mission_name,
        'MYSELF_Longitude': myself_longitude,
        'MYSELF_Latitude': myself_latitude,
        'time': myself_timer
    }
    # 生成Mission ID
    missionId = str(uuid.uuid4())
    mission_data_str = json.dumps(mission_data)  # 將字典轉換為字串
    redis_db.hmset('missions', {missionId: mission_data_str})

    mission_data['missionId'] = missionId
    forwardData2MissionCalculator(json.dumps(mission_data))
    
    return 'Mission has been created successfully.', 200


@mission_blueprint.route("update/<string:missionId>", methods=['PUT'])
def update_mission(missionId):
    mission_data = request.get_json()
    original_mission_data = redis_db.hget("missions", missionId)
    original_mission_data = json.loads(original_mission_data.decode('utf-8')) 
    mission_data['time'] = original_mission_data['time']
    mission_data_str = json.dumps(mission_data)  # 將字典轉換為字串
    redis_db.hmset('missions', {missionId: mission_data_str})

    mission_data['missionId'] = missionId
    forwardData2MissionCalculator(json.dumps(mission_data))
    
    return 'Mission has been updated successfully.', 200


@mission_blueprint.route("delete/<string:missionId>", methods=["DELETE"])
def delete_mission(missionId):
    # 檢查missionid是否存在
    if redis_db.hexists('missions', missionId):
        redis_db.hdel('missions', missionId)
        return "Ok", 200
    else:
        return "not found", 404
    
def forwardData2MissionCalculator(json_data):
    print(json_data)
    headers = {'Content-type': 'application/json'}
    conn.request('POST', '/path/to/resource', body=json_data, headers=headers)
    res = conn.getresponse()
    data = res.read().decode()