import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# 定义 Redis Sentinel 的地址和端口
sentinel_host = 'redis-sentinel.redis-i2.svc.cluster.local'
sentinel_port = 26379


# 定义请求处理类，继承自 BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    # 处理 GET 请求
    def do_GET(self):
        # 设置响应状态码为 200 OK
        self.send_response(200)
        # 设置响应头
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # 检查 Redis Sentinel
        if check_redis_sentinel():
            # 如果 Redis Sentinel 存在，返回 OK
            self.wfile.write(b'exporter_status{service="redis"} 1\n')
        else:
            # 如果 Redis Sentinel 不存在，返回 NOT OK
            self.wfile.write(b'exporter_status{service="redis"} 0\n')

# 定义检查 Redis Sentinel 函数
def check_redis_sentinel():
    try:
        # 创建 socket 连接到 Redis Sentinel
        with socket.create_connection((sentinel_host, sentinel_port), timeout=5) as sock:
            return True
    except Exception as e:
        print(f'Error checking Redis Sentinel: {str(e)}')
        return False

# 定义主程序
def main():
    try:
        # 创建 HTTP 服务器，并指定请求处理类为上面定义的 RequestHandler
        server = HTTPServer(('0.0.0.0', 51921), RequestHandler)
        print('Starting exporter server on port 51921...')
        # 启动 HTTP 服务器，持续监听请求
        server.serve_forever()
    except KeyboardInterrupt:
        # 捕获 Ctrl+C 中断信号，关闭服务器
        print('Stopping exporter server...')
        server.socket.close()

# 如果当前脚本为主程序，则执行 main 函数
if __name__ == '__main__':
    main()
