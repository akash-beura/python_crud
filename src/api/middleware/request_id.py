import uuid
from contextvars import ContextVar

from fastapi import Request

REQUEST_ID_HEADER = "X-Request-ID"

# Lets any code (logging, repositories) read the current request's id
# without passing it around, similar to MDC in Java.
request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


async def add_request_id(request: Request, call_next):
    # Reuse the caller's id if given (e.g. from a gateway), else generate one.
    request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())

    request.state.request_id = request_id
    token = request_id_ctx.set(request_id)
    try:
        response = await call_next(request)
    finally:
        request_id_ctx.reset(token)

    response.headers[REQUEST_ID_HEADER] = request_id
    return response
