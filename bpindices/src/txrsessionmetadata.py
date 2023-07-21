from dataclasses import dataclass
import datetime


@dataclass
class TxrSessionMetadata:
    id: str
    age: int
    gender: str
    beginTime: str
    originalFile: str

