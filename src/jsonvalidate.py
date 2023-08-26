# -*- coding: UTF-8 -*-

from jsonschema import validate
import json

schema_channel = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Channels",
    "description": "Channels configuration description",
    "type": "object",
    "properties": {
        "channels": {
            "required": ["nb", "name", "is_enable", "progdays"],
            "description": "Channel configuration",
            "properties": {
                "nb": {
                    "description": "Channel number",
                    "type": "integer",
                    "minimum": 0,
                },
                "name": {
                    "description": "Channel name",
                    "type": "string",
                },
                "is_enable": {
                    "description": "Set channel enable or not",
                    "type": "boolean",
                },
                "progdays": {
                    "description": "Programmation settings (day and time)",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["is_active", "days", "stime"],
                        "properties": {
                            "is_active": {
                                "description":
                                "Activation of current progam",
                                "type": "boolean",
                            },
                            "days": {
                                "description": "Program active days",
                                "type": "array",
                                "minItems": 7,
                                "maxItems": 7,
                                "items": {
                                    "type": "boolean",
                                },
                            },
                            "stime": {
                                "description": "Time program",
                                "required":
                                ["hour", "minute", "duration"],
                                "properties": {
                                    "hour": {
                                        "type": "integer",
                                        "minimum": 0,
                                        "maximum": 23,
                                    },
                                    "minute": {
                                        "type": "integer",
                                        "minimum": 0,
                                        "maximum": 59,
                                    },
                                    "duration": {
                                        "type": "integer",
                                        "minimum": 0,
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }
}

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Channels",
    "description": "Channels configuration description",
    "type": "object",
    "properties": {
        "channels": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["nb", "name", "is_enable", "progdays"],
                "properties": {
                    "nb": {
                        "description": "Channel number",
                        "type": "integer",
                        "minimum": 0,
                        "uniqueItems": True,
                    },
                    "name": {
                        "description": "Channel name",
                        "type": "string",
                    },
                    "is_enable": {
                        "description": "Set channel enable or not",
                        "type": "boolean",
                    },
                    "progdays": {
                        "description": "Programmation settings (day and time)",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["is_active", "days", "stime"],
                            "properties": {
                                "is_active": {
                                    "description":
                                    "Activation of current progam",
                                    "type": "boolean",
                                },
                                "days": {
                                    "description": "Program active days",
                                    "type": "array",
                                    "minItems": 7,
                                    "maxItems": 7,
                                    "items": {
                                        "type": "boolean",
                                    },
                                },
                                "stime": {
                                    "description": "Time program",
                                    "required":
                                    ["hour", "minute", "duration"],
                                    "properties": {
                                        "hour": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 23,
                                        },
                                        "minute": {
                                            "type": "integer",
                                            "minimum": 0,
                                            "maximum": 59,
                                        },
                                        "duration": {
                                            "type": "integer",
                                            "minimum": 0,
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            "minItems": 1,
        },
    },
    "required": ["channels"],
}

raspberry = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Channels",
    "description": "Channels configuration description",
    "type": "object",
    "properties": {
        "channels": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["channel", "pin"],
                "property": {
                    "channel": {
                        "type": "number"
                    },
                    "pin": {
                        "type": "number"
                    }
                }
            }
        },
        "water_level": {
            "type": "object",
            "properties": {
                "pin": {
                    "type": "number"
                },
                "inverted": {
                    "type": "boolean"
                }
            },
            "required": ["pin", "inverted"]
        }
    },
    "required": ["channels", "water_level"]
}


class Validate():
    """ Validate JSON database against
    """

    def __init__(self):
        pass

    def validate_file(self, filename):
        """ Validate JSON file
        @param filenbame: full path to JSON file
        raise an excpetion in case of error
        @return: JSON object
        """
        with open(filename, "r") as fd:
            json_string = fd.read()
            json_object = json.loads(json_string)
            validate(json_object, schema)
        return json_object

    def validate_string(self, data):
        """ Validate JSON string
        @param data: JSON string
        @return: JSON object
        """
        json_object = json.loads(data)
        validate(json_object, schema)
        return json_object

    def validate_json(self, json):
        """ Validate JSON object
        @param json: JSON object
        @return: JSON object
        """
        validate(json, schema)
        return json

    def validate_channel(self, json):
        validate(json, schema_channel)
        return json

    def validate_raspberry(self, json):
        validate(json, raspberry)
        return json
