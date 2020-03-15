from copy import deepcopy

import pytest

from cerberus_list_schema import Validator
from cerberus_list_schema.tests.test_data.list_schemas import simple_list_schema, extended_list_schema
from cerberus_list_schema.tests.test_data.dict_schemas import simple_dict_schema, extended_dict_schema


def test_simple_list_validation_works():
    document = ['test1', 600, 'test2']
    v = Validator(simple_list_schema)
    o = v.normalized_as_object(document, callable_numbers=False)
    p = v.normalized_as_object(document, callable_numbers=True)
    assert(o[0] == 'test1')
    assert(o[1] == 600)
    assert(o[2] == 'test2')
    assert(p._0 == 'test1')
    assert(p._1 == 600)
    assert(p._2 == 'test2')


def test_simple_dict_validation_works():
    document = {'list_of_values': ['test1', 600, 'test2']}
    v = Validator(simple_dict_schema)
    o = v.normalized_as_object(document, callable_numbers=False)
    p = v.normalized_as_object(document, callable_numbers=True)
    assert(o.hello[0] == 'test1')
    assert(o.hello[1] == 600)
    assert(o.hello[2] == 'test2')
    assert(o['hello'][0] == 'test1')
    assert(o['hello'][1] == 600)
    assert(o['hello'][2] == 'test2')
    assert(p.hello._0 == 'test1')
    assert(p.hello._1 == 600)
    assert(p.hello._2 == 'test2')
    assert(p['hello']['_0'] == 'test1')
    assert(p['hello']['_1'] == 600)
    assert(p['hello']['_2'] == 'test2')


def test_extended_list_validation_works():
    document = [
        ['test1', 501, ['test2', 1, 2, 55]],
        600,
        ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ['test10', 600, 'test11']
    ]
    v = Validator(extended_list_schema)
    o = v.normalized_as_object(document, callable_numbers=False)
    p = v.normalized_as_object(document, callable_numbers=True)
    assert(o[0][2].second_int == 1)
    assert (p._0._2.second_int == 1)
    assert (o[2][3].field01231 == 'testfield')
    assert (p._2._3.field01231 == 'testfield')
    assert (o[2][3].field2 == 5)
    assert (p._2._3.field2 == 5)
    assert (o.hello[1] == 600)
    assert (p.hello._1 == 600)


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
    o = v.normalized_as_object(document, callable_numbers=False)
    p = v.normalized_as_object(document, callable_numbers=True)
    assert(o.list_of_values_2['3'].second_int == 1)
    assert (p.list_of_values_2._3.second_int == 1)
    assert (o.first_val[2][3].field01231 == 'testfield')
    assert (p.first_val._2._3.field01231 == 'testfield')
    assert (o.first_val[2][3].field2 == 5)
    assert (p.first_val._2._3.field2 == 5)
    assert (o.hello[1] == 600)
    assert (p.hello._1 == 600)


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
        v.normalized_as_object(document)

    v.normalized_as_dict(document, allow_name_conflicts=True)
