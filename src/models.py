import attr
import cattr
from typing import Optional, Any


@attr.s(auto_attribs=True)
class Condition:
    attribute_name: str
    operator: str
    value: Optional[Any]

    @classmethod
    def from_dict(cls, dictionary: dict):
        return cattr.structure(dictionary, cls)
