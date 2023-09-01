from dataclasses import dataclass


@dataclass
class TxrSessionMetadata:
    id: str
    age: int
    gender: str
    beginTime: str
    originalFile: str

