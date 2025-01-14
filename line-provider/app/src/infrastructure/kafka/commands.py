from enum import Enum


class KafkaCommand(str, Enum):
    GET_ALL_EVENTS = "GET_ALL_EVENTS"
    GET_EVENT = "GET_EVENT"
