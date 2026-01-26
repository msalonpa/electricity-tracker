from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Min15Point:
    time: str
    value: float
    min15Points: List['Min15Point']  # Recursive, but in example it's empty

    @classmethod
    def from_dict(cls, data: dict) -> 'Min15Point':
        min15_points = data.get('min15Points', [])
        if not isinstance(min15_points, list):
            min15_points = []
        return cls(
            time=data.get('time', ''),
            value=data.get('value', 0.0),
            min15Points=[cls.from_dict(p) for p in min15_points]
        )

@dataclass
class HourData:
    time: str
    value: float
    min15Points: List[Min15Point]

    @classmethod
    def from_dict(cls, data: dict) -> 'HourData':
        min15_points = data.get('min15Points', [])
        if not isinstance(min15_points, list):
            min15_points = []
        return cls(
            time=data.get('time', ''),
            value=data.get('value', 0.0),
            min15Points=[Min15Point.from_dict(p) for p in min15_points]
        )

@dataclass
class PriceData:
    hour: List[HourData]

    @classmethod
    def from_dict(cls, data: dict) -> 'PriceData':
        hours = data.get('hour', [])
        if not isinstance(hours, list):
            hours = []
        return cls(
            hour=[HourData.from_dict(h) for h in hours]
        )

# Example usage:
# import json
# with open('price_data.json', 'r') as f:
#     data = json.load(f)
# price_data = PriceData.from_dict(data)
