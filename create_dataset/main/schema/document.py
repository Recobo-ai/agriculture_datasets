from typing import Any, Optional, Dict
from uuid import uuid4


class Document:
    def __init__(self, text: str,
                 id: str = None,
                 meta: Optional[Dict[str, Any]] = dict()):
        self.text = text
        # Create a unique ID (either new one, or one from user input)
        if id:
            self.id = str(id)
        else:
            self.id = str(uuid4())

        self.meta = meta

    def to_dict(self, field_map={'text', 'meta'}):
        inv_field_map = {v: k for k, v in field_map.items()}
        print(f"inv_field_map: {inv_field_map}")
        _doc: Dict[str, str] = {}
        for k, v in self.__dict__.items():
            print(f"{k}, {v}")
            k = k if k not in inv_field_map else inv_field_map[k]
            _doc[k] = v
        print(f"final: {_doc}")
        return _doc

    def __str__(self):
        return str(self.to_dict())

    @classmethod
    def from_dict(cls, dict):
        _doc = dict.copy()
        init_args = ["text", "id", "score", "meta"]
        if "meta" not in _doc.keys():
            _doc["meta"] = {}
        _new_doc = {}
        for k, v in _doc.items():
            if k in init_args:
                _new_doc[k] = v

        return cls(**_new_doc)
