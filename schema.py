bound_message_schema = {
            "$schema": "http://json-schema.org/draft-06/schema#",
            "title": "newBounds message",
            "description": "Message with bound of visible part of map",
            "type": "object",
            "properties": {
                "msgType": {
                    "const": "newBounds",
                    "description": "Message type",
                    "type": "string"
                },
                "data": {
                    "type": "object",
                    "properties": {
                        "east_lng": {
                            "type": "number",
                            "minimum": -90,
                            "maximum": 0
                        },
                        "north_lat": {
                            "type": "number",
                            "minimum": -90,
                            "maximum": 0
                        },
                        "south_lat": {
                            "type": "number",
                            "minimum": -90,
                            "maximum": 90
                        },
                        "west_lng": {
                            "type": "number",
                            "minimum": -90,
                            "maximum": 90
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "east_lng",
                        "north_lat",
                        "south_lat",
                        "west_lng"
                    ]
                }
            },
            "additionalProperties": False,
            "required": ["msgType", "data"]
}
bus = {
  "msgType": "Buses",
  "buses": [
    {"busId": "c790сс", "lat": 55.7500, "lng": 37.600, "route": "120"},
    {"busId": "a134aa", "lat": 55.7494, "lng": 37.621, "route": "120"},
  ]
}

bus_message_schema = {
            "$schema": "http://json-schema.org/draft-06/schema#",
            "title": "Buses message",
            "description": "Message with geopoints of buses",
            "type": "object",
            "properties": {
                "msgType": {
                    "const": "Buses",
                    "description": "Message type",
                    "type": "string"
                },
                "buses": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "busId": {
                                "type": "string"
                            },
                            "lat": {
                                "type": "number",
                                "minimum": -90,
                                "maximum": 90
                            },
                            "lng": {
                                "type": "number",
                                "minimum": -90,
                                "maximum": 90
                            },
                            "route": {
                                "type": "string"
                            }
                        },
                        "additionalProperties": False,
                        "required": ["lng", "lat", "route", "busId"]
                    }
                }
            },
            "additionalProperties": False,
            "required": ["msgType", "buses"]
}
from jsonschema import validate

print(validate(bus, bus_message_schema))