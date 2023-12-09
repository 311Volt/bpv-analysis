from dataclasses import dataclass


@dataclass
class TxrSessionMetadata:
    id: str
    age: int
    gender: str
    bmiValue : float
    waistToHip : float
    drugsQuantity : int
    illnessDuration : int
    beginTime: str
    originalFile: str

