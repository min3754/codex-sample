import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


def echo(message: str) -> str:
    """Return the same message provided by the client."""
    return message


def current_time() -> str:
    """Return the current server time."""
    return time.ctime()


def add_numbers(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


class MCPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != '/sse':
            self.send_error(404)
            return

        params = parse_qs(parsed.query)
        fn = params.get('fn', [''])[0]

        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.end_headers()

        if fn == 'echo':
            message = params.get('msg', [''])[0]
            result = echo(message)
            self.wfile.write(f"data: {result}\n\n".encode('utf-8'))
        elif fn == 'time':
            # stream three updates one second apart
            for _ in range(3):
                result = current_time()
                self.wfile.write(f"data: {result}\n\n".encode('utf-8'))
                self.wfile.flush()
                time.sleep(1)
        elif fn == 'sum':
            try:
                a = float(params.get('a', ['0'])[0])
                b = float(params.get('b', ['0'])[0])
                result = add_numbers(a, b)
                self.wfile.write(f"data: {result}\n\n".encode('utf-8'))
            except ValueError:
                self.wfile.write(b"data: invalid parameters\n\n")
        else:
            self.wfile.write(b"data: unknown function\n\n")


def run(server_class=HTTPServer, handler_class=MCPHandler, port: int = 8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"MCP SSE server running on port {port}")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
