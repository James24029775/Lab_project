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



class RequestHandler(BaseHTTPRequestHandler):
    
    protocol_version = 'HTTP/1.1'
    i = 0
    ms_coordinate_x = -1
    ms_coordinate_y = -1
    def do_POST(self):
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        print(post_body)
        data = json.loads(post_body)
        self.ms_coordinate_x = data["coordinate_x"]
        self.ms_coordinate_y = data["coordinate_y"]
        print(self.ms_coordinate_x)
        print(self.ms_coordinate_y)
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
