# backend/api/logs.py
import pathlib, asyncio, time
from django.http import StreamingHttpResponse

LOG = pathlib.Path("logs/burza.log")

async def event_stream():
    with LOG.open() as f:
        f.seek(0,2)                     # tail
        while True:
            line = f.readline()
            if line:
                yield f"data: {line}\n\n"
            else:
                await asyncio.sleep(0.5)

def log_stream(request):
    return StreamingHttpResponse(event_stream(),
                                 content_type="text/event-stream")
