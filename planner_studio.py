#!/usr/bin/env python3
"""Run Planner Studio locally and connect it to planner_factory."""
import argparse, json, webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import planner_factory
ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT/'studio'),**kw)
    def log_message(self,*a): pass
    def send_json(self,data,status=200):
        body=json.dumps(data).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path=='/api/health': return self.send_json({'ok':True,'version':planner_factory.VERSION})
        if self.path=='/': self.path='/index.html'
        super().do_GET()
    def do_POST(self):
        try: spec=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
        except Exception as exc: return self.send_json({'error':str(exc)},400)
        findings=planner_factory.validate(spec); valid=not any(x.startswith('ERROR') for x in findings)
        if self.path=='/api/validate': return self.send_json({'valid':valid,'findings':findings})
        if self.path=='/api/render':
            if not valid: return self.send_json({'error':'Fix validation errors before exporting.','findings':findings},422)
            body=planner_factory.render(spec).encode(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Disposition','attachment; filename="planner.html"'); self.send_header('Content-Length',str(len(body))); self.end_headers(); return self.wfile.write(body)
        self.send_json({'error':'Not found'},404)
def main():
    p=argparse.ArgumentParser(description='Run Planner Studio locally.'); p.add_argument('--host',default='127.0.0.1'); p.add_argument('--port',type=int,default=8765); p.add_argument('--no-browser',action='store_true'); a=p.parse_args(); server=ThreadingHTTPServer((a.host,a.port),Handler); url=f'http://{a.host}:{a.port}'; print(f'Planner Studio is ready at {url} — press Ctrl+C to stop.');
    if not a.no_browser: webbrowser.open(url)
    try: server.serve_forever()
    except KeyboardInterrupt: print('\nPlanner Studio stopped.')
    finally: server.server_close()
if __name__=='__main__': main()
