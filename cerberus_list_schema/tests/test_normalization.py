from cerberus_list_schema import Validator
from cerberus_list_schema.tests.test_data.utils import (
    get_extended_dict_schema,
    get_extended_list_schema,
    get_simple_dict_schema,
    get_simple_list_schema,
)


def test_simple_list_validation_works():
    document = ["test1", 600, "test2"]
    schema = get_simple_list_schema()

    v = Validator(schema)
    assert v.normalized(document) == ["test1", 600, "test2"]
    assert v.errors == {}


def test_simple_dict_validation_works():
    document = {"list_of_values": ["test1", 600, "test2"]}
    schema = get_simple_dict_schema()

    v = Validator(schema)
    assert v.normalized(document) == {"list_of_values": ["test1", 600, "test2"]}
    assert v.errors == {}


def test_extended_list_validation_works():
    document = [
        ["test1", 501, ["test2", 1, 2, 55]],
        600,
        ["test3", 1, 2, {"field1": "testfield", "field2": 5}],
        ["test10", 600, "test11"],
    ]
    schema = get_extended_list_schema()

    v = Validator(schema)
    assert v.normalized(document) == document
    assert v.errors == {}


def test_extended_dict_validation_works():
    document = {
        "list_of_values": [
            "test1",
            600,
            ["test3", 1, 2, {"field1": "testfield", "field2": 5}],
        ],
        "list_of_values_2": {"1": "test1", "2": 501, "3": ["test2", 1, 2, 55]},
        "list_of_values_3": ["test10", 600, "test11"],
    }
    schema = get_extended_dict_schema()

    v = Validator(schema)
    assert v.normalized(document) == document
    assert v.errors == {}


def test_normalization_rules_work():
    document = {
        "list_of_values": [
            "test1",
            600,
            [None, "1", 2, {"field1": "testfield", "field2": 5, "field3": "purge_me"}],
        ],
        "list_of_values_2": {"1": "test1", "2": 501, "3": ["test2", 1, 2, 55]},
        "list_of_values_3": ["test10", 600, "test11"],
    }
    expected_document = {
        "list_of_values": [
            "test1",
            600,
            ["test_default", 1, 2, {"field1": "testfield", "field2": 5}],
        ],
        "list_of_values_2": {"1": "test1", "2": 501, "3": ["test2", 1, 2, 55]},
        "list_of_values_3": ["test10", 600, "test11"],
    }
    schema = get_extended_dict_schema()

    v = Validator(schema, purge_unknown=True)
    assert v.normalized(document) == expected_document
    assert v.errors == {}


def test_normalization_rules_work_no_validator_init():
    document = {
        "list_of_values": [
            "test1",
            600,
            [None, "1", 2, {"field1": "testfield", "field2": 5, "field3": "purge_me"}],
        ],
        "list_of_values_2": {"1": "test1", "2": 501, "3": ["test2", 1, 2, 55]},
        "list_of_values_3": ["test10", 600, "test11"],
    }
    expected_document = {
        "list_of_values": [
            "test1",
            600,
            ["test_default", 1, 2, {"field1": "testfield", "field2": 5}],
        ],
        "list_of_values_2": {"1": "test1", "2": 501, "3": ["test2", 1, 2, 55]},
        "list_of_values_3": ["test10", 600, "test11"],
    }
    schema = get_extended_dict_schema()
    v = Validator(purge_unknown=True)
    assert v.normalized(document, schema) == expected_document
    assert v.errors == {}
