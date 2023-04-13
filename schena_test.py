from jsonschema import validate

schema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "newBounds message",
            "description": "Message from browser with bound of visible part of map",
            "type": "object",
            "properties": {
                "msgType": {
                    "description": "Message type",
                    "type": "string"
                },
                "data" : {
                    "type": "object",
                    "properties": {
                        "east_lng": {"type": "number"},
                        "north_lat":{"type": "number"},
                        "south_lat": {"type": "number"},
                        "west_lng": {"type": "number"}
                    },
                    "additionalProperties": False,
                    "required": ["east_lng", "north_lat", "south_lat", "west_lng"]
                }
            },
    "required": ["msgType", "data"]
}


message = {
  "msgType": "newBounds",
  "data": {
    "east_lng": 37.65563964843751,
    "north_lat": 55.77367652953477,
    "south_lat": 55.72628839374007,
    "west_lng": 37.54440307617188,
    "dd": 55,
}
}

print(validate(message, schema))
