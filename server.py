import http.server
import json
import urllib.request
import urllib.error
import os
import sys

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
PORT = 8080

if not API_KEY:
    print("ERROR: ANTHROPIC_API_KEY is not set.")
    print('Add this line to ~/.zshrc, then open a new Terminal window:')
    print('  export ANTHROPIC_API_KEY="sk-ant-..."')
    sys.exit(1)


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        if self.path != "/api":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                self.send_json(200, resp.read())
        except urllib.error.HTTPError as e:
            result = e.read()
            print(f"Anthropic API error {e.code}: {result.decode(errors='replace')}")
            self.send_json(e.code, result)
        except Exception as e:
            print(f"Server error: {e}")
            msg = {"type": "error", "error": {"message": f"Server error: {e}"}}
            self.send_json(500, json.dumps(msg).encode())

    def log_message(self, format, *args):
        pass


print(f"OriginDocs running at http://localhost:{PORT}/origindocs.html")
print("Press Ctrl+C to stop.\n")
httpd = http.server.HTTPServer(("", PORT), Handler)
httpd.serve_forever()
