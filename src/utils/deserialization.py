from typing import Any

def deserialize_binary(serialized_data: bytes) -> Any:
    return serialized_data.decode('utf-8')
