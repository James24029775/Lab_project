# import
from pymongo import MongoClient
from bson.objectid import ObjectId #這東西再透過ObjectID去尋找的時候會用到
from pprint import pprint
import http.client
import json


def main():
    # 建立 MongoDB 伺服器的連線
    client = MongoClient('localhost', 27017)

    # 選擇要使用的資料庫
    db = client['free5gc']

    # 選擇要使用的資料庫和 collection
    collection = db['tenantData']

    transmitt_all(collection)

def transmitt_all(collection):
    i = 1
    # 查詢 collection 中的所有資料
    for document in collection.find():
        # tmp_data = collection.find_one({'missionId': '7e81b221-ebea-4887-9047-8aa7f833bb3c'})

        # 將 ObjectId 轉換為字串
        document['_id'] = str(document['_id'])

        # 將字典轉換為 JSON 字符串
        json_data = json.dumps(document)

        # # 輸出 JSON 字符串
        # print(json_data)

        # 設置請求頭部
        headers = {'Content-type': 'application/json'}

        # 建立連接
        conn = http.client.HTTPConnection('localhost', 7000)

        # 發送請求
        conn.request('POST', '/path/to/resource', body=json_data, headers=headers)

        # 讀取響應
        res = conn.getresponse()
        data = res.read().decode()

        # 關閉連接
        conn.close()

        print("Data", i, data)
        i += 1

if __name__ == '__main__':
    main()