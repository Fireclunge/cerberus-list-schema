from copy import deepcopy

import pytest

from cerberus_list_schema import Validator
from cerberus_list_schema.tests.test_data.dict_schemas import simple_dict_schema, extended_dict_schema
from cerberus_list_schema.tests.test_data.list_schemas import simple_list_schema, extended_list_schema


def test_simple_list_validation_works():
    document = ['test1', 600, 'test2']
    v = Validator(simple_list_schema)
    assert (v.normalized_as_dict(document) == {0: 'test1', 1: 600, 2: 'test2'})
    assert (v.errors == {})


def test_simple_dict_validation_works():
    document = {'list_of_values': ['test1', 600, 'test2']}
    v = Validator(simple_dict_schema)
    assert (v.normalized_as_dict(document) == {'hello': {0: 'test1', 1: 600, 2: 'test2'}})
    assert (v.errors == {})


def test_extended_list_validation_works():
    document = [
        ['test1', 501, ['test2', 1, 2, 55]],
        600,
        ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ['test10', 600, 'test11']
    ]
    v = Validator(extended_list_schema)
    assert (v.normalized_as_dict(document) == {
        0: {0: 'test1', 1: 501, 2: {0: 'test2', 'second_int': 1, 2: 2, 3: 55}},
        1: 600,
        2: {0: 'test3', 1: 1, 'hi': 2, 3: {'field01231': 'testfield', 'field2': 5}},
        'hello': {0: 'test10', 1: 600, 2: 'test11'}
    })
    assert (v.errors == {})


def test_extended_dict_validation_works():
    document = {
        'list_of_values': [
            'test1',
            600,
            ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 501, '3': ['test2', 1, 2, 55]},
        'list_of_values_3': ['test10', 600, 'test11']
    }
    v = Validator(extended_dict_schema)
    assert (v.normalized_as_dict(document) == {
        'first_val': {0: 'test1', 1: 600, 2: {0: 'test3', 1: 1, 'hi': 2, 3: {'field01231': 'testfield', 'field2': 5}}},
        'list_of_values_2': {'1': 'test1', '2': 501, '3': {0: 'test2', 'second_int': 1, 2: 2, 3: 55}},
        'hello': {0: 'test10', 1: 600, 2: 'test11'}
    })
    assert (v.errors == {})


def test_conflicting_dict_name_fails():
    document = {
        'list_of_values': [
            'test1',
            600,
            ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 501, '3': ['test2', 1, 2, 55]},
        'list_of_values_3': ['test10', 600, 'test11']
    }

    dict_schema = deepcopy(extended_dict_schema)

    dict_schema['list_of_values']['name'] = 'hello'
    v = Validator(dict_schema)
    with pytest.raises(AttributeError):
        v.normalized_as_dict(document)

    assert (v.normalized_as_dict(document, allow_name_conflicts=True) == {
        'list_of_values_2': {'1': 'test1', '2': 501, '3': {0: 'test2', 'second_int': 1, 2: 2, 3: 55}},
        'hello': {0: 'test10', 1: 600, 2: 'test11'}
    })
    assert (v.errors == {})
