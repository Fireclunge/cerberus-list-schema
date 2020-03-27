from cerberus_list_schema import Validator
from cerberus_list_schema.tests.test_data.utils import get_multiuse_schema


def test_multiuse_validation_works():
    document = {
        "list_of_values": [
            "rawr",
            1000,
            ["sfsdf", 1, 4, {"field1": "dasdsa", "field2": 3, "field3": "sfd"}],
        ],
        "list_of_values_2": ["fd", 1000, ["sfsdf", 1, 5434, 4, 4]],
    }
    schema = get_multiuse_schema()

    v = Validator(schema, allow_list_missing=True)

    for i in range(3):
        # -------------------------------------------------------------------------------------------------------
        expected_value = {
            "list_of_values": [{2: [{3: [{"field3": ["unknown field"]}]}]}],
            "list_of_values_2": [{2: [{3: ["min value is 50"], 4: ["unknown field"]}]}],
        }
        assert v.validate(document) is False
        assert v.errors == expected_value
        assert v.validate(document, schema) is False
        assert v.errors == expected_value

        # -------------------------------------------------------------------------------------------------------
        expected_value = {
            "list_of_values": [
                "rawr",
                1000,
                ["sfsdf", 1, 4, {"field1": "dasdsa", "field2": 3, "field3": "sfd"}],
            ],
            "list_of_values_2": ["fd", 1000, ["sfsdf", 1, 5434, 4, 4]],
        }
        assert v.normalized(document) == expected_value
        assert v.normalized(document, schema) == expected_value

        # -------------------------------------------------------------------------------------------------------
        expected_value = {
            "hello": {
                0: "rawr",
                1: 1000,
                2: {
                    0: "sfsdf",
                    1: 1,
                    "hi": 4,
                    3: {"field01231": "dasdsa", "field2": 3, "field3": "sfd"},
                },
            },
            "list_of_values_2": {
                0: "fd",
                1: 1000,
                2: {0: "sfsdf", "nd_int": 1, 2: 5434, 3: 4, 4: 4},
            },
        }
        assert v.normalized_as_dict(document) == expected_value
        assert v.normalized_as_dict(document, schema) == expected_value

        a = v.normalized_as_object(document)
        b = v.normalized_as_object(document, schema)

        assert a.hello[2].hi == 4
        assert b.hello[2].hi == 4

        assert a.list_of_values_2[2].nd_int == 1
        assert a.list_of_values_2[2].nd_int == 1

        assert a.list_of_values_2[2][2] == 5434
        assert a.list_of_values_2[2][2] == 5434
