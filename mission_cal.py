from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPConnection
from urllib.parse import urlparse
import json
import http.client
import threading
from socketserver import ThreadingMixIn
import logging
import redis
import socket

msg = "I HAVE RECEIVED THE NEWEST MISSION INSTRUCTION!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

class RequestHandler(BaseHTTPRequestHandler):
    
    protocol_version = 'HTTP/1.1'
    i = 0
    ms_coordinate_x = -1
    ms_coordinate_y = -1

    # 收到封包後觸發
    def do_POST(self):
        # 從header讀取body長度並抽出資料
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        print(post_body)

        # 以JSON解析資料
        data = json.loads(post_body)
        self.ms_ID = data['missionId']
        self.ms_name = data['missionName']
        self.ms_coordinate_x = data["MYSELF_Longitude"]
        self.ms_coordinate_y = data["MYSELF_Latitude"]
        print(msg)
        print("ID:\t\t", self.ms_ID)
        print("Name:\t\t", self.ms_name)
        print("Longitude:\t", self.ms_coordinate_x)
        print("Latitude:\t", self.ms_coordinate_y)
        print("*"*len(msg))

        # 向client回覆ok訊息
        response_data = '{"response": "ok"}'
        self.send_response(200)
        self.send_header('Content-length', len(response_data))
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        self.wfile.write(json.dumps({
            'response': "ok"
        }).encode())
        #threading.Thread(target = self.clientHandler).start()
                    
        
            
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', 7000), RequestHandler)
    server.serve_forever()
