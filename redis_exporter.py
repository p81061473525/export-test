import ast
import socketserver
import http.server
import socket
import time

def load_redis_instances_from_file(filename):
    redis_instances = []
    with open(filename, 'r') as file:
        for line in file:
            entry = ast.literal_eval(line.strip())
            redis_instances.append(entry)
    return redis_instances

# 由於 REDIS_INSTANCES 需要函式 load_redis_instances_from_file 先存在，變數只好放這邊，不放頭
REDIS_INSTANCES = load_redis_instances_from_file('total.txt')

def check_redis_instance(host, port):
    try:
        # Create a socket connection to the Redis instance
        with socket.create_connection((host, port), timeout=2) as conn:
            # Connection successful, return True
            return True
    except Exception as e:
        # Connection failed, return False
        return False

def generate_prometheus_metrics(instance, available):
    service_name = instance["service"]
    if available:
        return f'redis_alive{{service="{service_name}"}} 1'
    else:
        return f'redis_alive{{service="{service_name}"}} 0'

def check_redis_status():
    result = ""
    # Iterate through each Redis instance and check its availability
    for instance in REDIS_INSTANCES:
        host = instance["host"]
        port = instance["port"]
        if check_redis_instance(host, port):
            metrics = generate_prometheus_metrics(instance, True)
            result += metrics + "\n"
        else:
            metrics = generate_prometheus_metrics(instance, False)
            result += metrics + "\n"
    return result.encode()

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(check_redis_status())
        else:
            super().do_GET()

def main():
    PORT = 51921
    server_address = ('', PORT)
    httpd = socketserver.TCPServer(server_address, MyHttpRequestHandler)
    print(f"Starting HTTP server on port {PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
