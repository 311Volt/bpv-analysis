from dataclasses import dataclass
import datetime


@dataclass
class TxrSessionMetadata:
    id: str
    age: int
    gender: str
    beginTime: str
    originalFile: str

    def beginTimeAsDatetime(self):
        return datetime.datetime.strptime(self.beginTime, "%Y-%m-%d %H:%M")

    def is_age_valid(self):
        return self.age < 100

    def is_male(self):
        return self.gender == "male"

    def is_female(self):
        return self.gender == "female"

