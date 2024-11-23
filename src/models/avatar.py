import hashlib
import json

from pydantic import BaseModel


class Avatar(BaseModel):
    pattern: str
    primary: str
    secondary: str

    def to_hash(self):
        data_to_hash = json.dumps({
            "pattern": self.pattern,
            "primary": self.primary,
            "secondary": self.secondary
        })
        return hashlib.md5(data_to_hash.encode()).hexdigest()
