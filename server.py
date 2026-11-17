import os
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

os.chdir("/workspace/calm-ramanujan")

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")
        sys.stderr.flush()

def run_port(port):
    try:
        server = HTTPServer(("0.0.0.0", port), Handler)
        print(f"TubeDZ server active on port {port}")
        sys.stdout.flush()
        server.serve_forever()
    except Exception as e:
        print(f"Port {port} error: {e}")
        sys.stdout.flush()

if __name__ == '__main__':
    t1 = threading.Thread(target=run_port, args=(8080,), daemon=True)
    t2 = threading.Thread(target=run_port, args=(3000,), daemon=True)
    t1.start()
    t2.start()
    t1.join()
