import requests

# 定義任務資料
mission_data = {
    'missionId': '1',
    'missionName': 'Mission 1',
    'MYSELF_Longitude': '123.456',
    'MYSELF_Latitude': '78.90'
}

# 呼叫 'mission' Redis API 來設定任務資料
response = requests.post('http://127.0.0.1:8080/mission/createmission', json=mission_data)

# /mission/getmission
# /mission/createmission

# 檢查回應狀態碼與內容
if response.status_code == 200:
    print('Mission has been set successfully.')
else:
    print('Failed to set mission:', response.json())


response = requests.get('http://127.0.0.1:8080/mission/getmission')

# 檢查回應狀態碼
if response.status_code == 200:
    # 解析回應內容為 JSON 格式
    missions = response.json()
    # 在這裡可以對取得的任務資料進行處理
    print('Missions:', missions['data'])
else:
    print('Failed to get missions. Status code:', response.status_code)