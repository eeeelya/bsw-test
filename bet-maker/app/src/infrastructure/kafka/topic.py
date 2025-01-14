from enum import Enum


class KafkaTopic(str, Enum):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
