import json
import math
from http import HTTPStatus

from urllib.parse import parse_qs


async def app(scope, receive, send) -> None:
    assert scope["type"] == "http"
    method = scope["method"]
    path = scope["path"]

    if method == "GET" and path == "/factorial":
        await factorial_handler(scope, receive, send)
    elif method == "GET" and path.startswith("/fibonacci"):
        await fibonacci_handler(scope, receive, send)
    elif method == "GET" and path == "/mean":
        await mean_handler(scope, receive, send)
    else:
        await not_found(send)


async def factorial_handler(scope, receive, send):
    query_string = scope.get("query_string", b"").decode()
    query_params = parse_qs(query_string)
    n_values = query_params.get("n")

    if not n_values:
        await unprocessable_entity(send)
        return

    try:
        n = int(n_values[0])
    except ValueError:
        await unprocessable_entity(send)
        return

    if n < 0:
        await bad_request(send, "Invalid value for n, must be non-negative")
        return

    result = math.factorial(n)
    await json_response(send, {"result": result})


async def fibonacci_handler(scope, receive, send):
    parts = scope["path"].split("/")
    if len(parts) < 3:
        await unprocessable_entity(send)
        return

    try:
        n = int(parts[2])
    except ValueError:
        await unprocessable_entity(send)
        return

    if n < 0:
        await bad_request(send, "Invalid value for n, must be non-negative")
        return

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    await json_response(send, {"result": b})


async def mean_handler(scope, receive, send):
    body = await get_request_body(receive)
    try:
        data = json.loads(body)
        if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
            raise ValueError
    except (json.JSONDecodeError, ValueError):
        await unprocessable_entity(send)
        return

    if not data:
        await bad_request(send, "Invalid value for body, must be non-empty array of floats")
        return

    result = sum(data) / len(data)
    await json_response(send, {"result": result})

async def get_request_body(receive):
    body = b""
    more_body = True
    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)
    return body.decode()

async def json_response(send, data, status=HTTPStatus.OK):
    response_body = json.dumps(data).encode()
    await send({
        "type": "http.response.start",
        "status": status,
        "headers": [
            (b"content-type", b"application/json"),
        ],
    })
    await send({
        "type": "http.response.body",
        "body": response_body,
    })

async def not_found(send):
    await send({
        "type": "http.response.start",
        "status": HTTPStatus.NOT_FOUND,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({
        "type": "http.response.body",
        "body": b"Not Found",
    })

async def bad_request(send, message):
    await send({
        "type": "http.response.start",
        "status": HTTPStatus.BAD_REQUEST,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({
        "type": "http.response.body",
        "body": message.encode(),
    })

async def unprocessable_entity(send):
    await send({
        "type": "http.response.start",
        "status": HTTPStatus.UNPROCESSABLE_ENTITY,
        "headers": [(b"content-type", b"text/plain")],
    })
    await send({
        "type": "http.response.body",
        "body": b"Unprocessable Entity",
    })
