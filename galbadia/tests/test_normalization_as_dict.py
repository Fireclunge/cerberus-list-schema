from galbadia import Validator
from galbadia.tests.test_data.list_schemas import simple_list_schema, extended_list_schema
from galbadia.tests.test_data.dict_schemas import simple_dict_schema, extended_dict_schema


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
    assert (v.normalized_as_dict(document) == document)
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
    assert (v.normalized_as_dict(document) == document)
    assert (v.errors == {})


def test_normalization_rules_work():
    document = {
        'list_of_values': [
            'test1',
            600,
            [None, '1', 2, {'field1': 'testfield', 'field2': 5, 'field3': 'purge_me'}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 501, '3': ['test2', 1, 2, 55]},
        'list_of_values_3': ['test10', 600, 'test11']
    }
    expected_document = {
        'list_of_values': [
            'test1',
            600,
            ['test_default', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 501, '3': ['test2', 1, 2, 55]},
        'list_of_values_3': ['test10', 600, 'test11']
    }
    v = Validator(extended_dict_schema, purge_unknown=True)
    assert (v.normalized_as_dict(document) == expected_document)
    assert (v.errors == {})

