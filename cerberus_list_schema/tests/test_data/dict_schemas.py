simple_dict_schema = {
    "list_of_values": {
        "type": "list",
        "name": "hello",
        "items": [
            {"type": "string"},
            {"type": "integer", "min": 500},
            {"type": "string"},
        ],
    }
}

# --------------------

other_schema = {
    "type": "dict",
    "schema": {
        "1": {"type": "string"},
        "2": {"type": "integer", "min": 500},
        "3": {
            "type": "list",
            "items": [
                {"type": "string"},
                {"type": "integer", "name": "second_int"},
                {"type": "integer"},
                {"type": "integer", "min": 50},
            ],
        },
    },
}

extended_dict_schema = {
    "list_of_values": {
        "type": "list",
        "name": "first_val",
        "items": [
            {"type": "string"},
            {"type": "integer", "min": 500},
            {
                "type": "list",
                "items": [
                    {"type": "string", "default": "test_default"},
                    {"type": "integer", "coerce": int},
                    {"type": "integer", "name": "hi"},
                    {
                        "type": "dict",
                        "schema": {
                            "field1": {"type": "string", "name": "field01231"},
                            "field2": {"type": "integer"},
                        },
                    },
                ],
            },
        ],
    },
    "list_of_values_2": other_schema,
    "list_of_values_3": simple_dict_schema["list_of_values"],
}
