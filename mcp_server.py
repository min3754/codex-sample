"""FastAPI-based implementation of the MCP SSE server."""

import asyncio
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI()


def echo(message: str) -> str:
    """Return the same message provided by the client."""
    return message


def current_time() -> str:
    """Return the current server time."""
    return time.ctime()


def add_numbers(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def _format_sse(data: str) -> str:
    """Format a string as an SSE event."""
    return f"data: {data}\n\n"


@app.get("/sse")
async def sse(fn: str, msg: str = "", a: float = 0.0, b: float = 0.0):
    """Serve different functions over server-sent events."""

    async def event_stream():
        if fn == "echo":
            yield _format_sse(echo(msg))
        elif fn == "time":
            for _ in range(3):
                yield _format_sse(current_time())
                await asyncio.sleep(1)
        elif fn == "sum":
            result = add_numbers(a, b)
            yield _format_sse(str(result))
        else:
            yield _format_sse("unknown function")

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mcp_server:app", host="0.0.0.0", port=8000)