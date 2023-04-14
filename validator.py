from jsonschema import Draft6Validator

BOUND_MESSAGE_SCHEMA = {
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
                    "maximum": 90
                },
                "north_lat": {
                    "type": "number",
                    "minimum": -90,
                    "maximum": 90
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

BUS_MESSAGE_SCHEMA = {
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


def validate_message(message, schema):
    validator = Draft6Validator(schema)
    errors = sorted(
        validator.iter_errors(message),
        key=lambda e: e.path
    )
    if errors:
        error_messages = []
        for error in errors:
            error_messages.append(error.message)
        return error_messages
    else:
        return None
