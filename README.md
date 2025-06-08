# codex-sample

This project provides a minimal example of an MCP (Message Control Protocol) server built with
[FastAPI](https://fastapi.tiangolo.com/) that streams results using Server-Sent Events (SSE). It
includes three simple example functions and exposes them through an HTTP endpoint.

## Running the server

Install the dependencies and run the server with Python 3.12 or later:

```bash
pip install -r requirements.txt
```

```bash
python3 mcp_server.py
```

The server listens on port `8000` by default and uses `uvicorn` under the hood.

## Example endpoints

- **Echo**: `http://localhost:8000/sse?fn=echo&msg=hello`
- **Current time**: `http://localhost:8000/sse?fn=time`
- **Add numbers**: `http://localhost:8000/sse?fn=sum&a=1&b=2`

Each endpoint returns responses as SSE events, making them easy to
consume from AI agents in tools such as Cursor or Claude Desktop.
