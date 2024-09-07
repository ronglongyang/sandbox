from typing import List, Dict
import json
from http.client import HTTPConnection


def send_post_request(
    conn: HTTPConnection,
    msgs: List[Dict[str, str]],
    api_endpoint: str = "/api/chat",
    model: str = "llama3.1",
    stream=False
):
    payload = json.dumps({
        "model": model,
        "messages": msgs,
        "stream": stream,
        "options": {
            "seed": 777,
            "temperature": 0
        },
    })
    conn.request(
        "POST",
        api_endpoint,
        body=payload,
        headers={"Content-Type": "application/json"}
    )
    return json.loads(
        conn.getresponse().read().decode()
    )


if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
    connection = HTTPConnection(..., ...)
    response = send_post_request(
        conn=connection,
        msgs=messages,
    )
    connection.close()
    print(response)
