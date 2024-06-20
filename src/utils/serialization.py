import json
from typing import Any


def json_serializer(data: Any) -> bytes:
    return json.dumps(data).encode('utf-8')

def string_serializer(data: str) -> bytes:
    return data.encode('utf-8')

def binary_serializer(data: bytes) -> bytes:
    return data
