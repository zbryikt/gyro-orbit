# 靜態伺服器: 雙協定 ( IPv4 + IPv6 ), 多執行緒, 連線佇列加大 -- 給 cloudflared 隧道大量並行請求用
import sys, socket, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
class Server(ThreadingHTTPServer):
  address_family = socket.AF_INET6
  request_queue_size = 256
  daemon_threads = True
  def server_bind(self):
    self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
    super().server_bind()
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8790
root = sys.argv[2] if len(sys.argv) > 2 else '.'
Server(('::', port), functools.partial(SimpleHTTPRequestHandler, directory=root)).serve_forever()
