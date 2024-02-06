from typing import Any


def is_param_valid(param: Any, expected_type: Any) -> bool:
    return param and isinstance(param, expected_type)
