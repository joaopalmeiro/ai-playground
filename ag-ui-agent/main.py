from collections.abc import AsyncIterator

from pydantic_ai.ui import SSE_CONTENT_TYPE
from pydantic_ai.ui.ag_ui import AGUIAdapter
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse
from starlette.routing import Route

from agent import agent


async def run_agent(request: Request) -> Response:
    body = await request.body()
    run_input = AGUIAdapter.build_run_input(body)

    adapter = AGUIAdapter(
        agent=agent,
        run_input=run_input,
        accept=SSE_CONTENT_TYPE,
    )

    async def logged() -> AsyncIterator[str]:
        print("<<< RESPONSE", end="\n" * 2)
        async for chunk in adapter.encode_stream(adapter.run_stream()):
            print(repr(chunk), end="\n" * 2)
            yield chunk

    return StreamingResponse(logged(), media_type=SSE_CONTENT_TYPE)


async def health(request: Request) -> Response:
    return JSONResponse({"status": "ok"})


app = Starlette(
    routes=[
        Route("/health", health),
        Route("/", run_agent, methods=["POST"]),
    ]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
