from galbadia import Validator
from galbadia.tests.test_data.list_schemas import simple_list_schema, extended_list_schema
from galbadia.tests.test_data.dict_schemas import simple_dict_schema, extended_dict_schema


# ----------------------------------------------------------------------------------------------------------------------

def test_simple_list_validation_works():
    document = ['test1', 600, 'test2']
    v = Validator(simple_list_schema)
    assert (v.validate(document) is True)
    assert (v.errors == {})


def test_simple_list_validation_breaks():
    document = [40, 600, 'test2']
    v = Validator(simple_list_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'_schema': [{0: ['must be of string type']}]})


def test_simple_list_validation_min_number_not_compliant():
    document = ['test1', 400, 'test2']
    v = Validator(simple_list_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'_schema': [{1: ['min value is 500']}]})


def test_simple_list_validation_list_len_breaks():
    document = ['test1', 600]
    v = Validator(simple_list_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'_schema': ['length of list should be 3, it is 2']})


def test_simple_list_validation_list_len_works():
    document = ['test1', 600]
    v = Validator(simple_list_schema, allow_list_missing=True)
    assert (v.validate(document) is True)
    assert (v.errors == {})


# ----------------------------------------------------------------------------------------------------------------------

def test_simple_dict_validation_works():
    document = {'list_of_values': ['test1', 600, 'test2']}
    v = Validator(simple_dict_schema)
    assert (v.validate(document) is True)
    assert (v.errors == {})


def test_simple_dict_validation_breaks():
    document = {'list_of_values': [40, 600, 'test2']}
    v = Validator(simple_dict_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'list_of_values': [{0: ['must be of string type']}]})


def test_simple_dict_validation_min_number_not_compliant():
    document = {'list_of_values': ['test1', 400, 'test2']}
    v = Validator(simple_dict_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'list_of_values': [{1: ['min value is 500']}]})


def test_simple_dict_validation_list_len_breaks():
    document = {'list_of_values': ['test1', 600]}
    v = Validator(simple_dict_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'list_of_values': ['length of list should be 3, it is 2']})


def test_simple_dict_validation_list_len_works():
    document = {'list_of_values': ['test1', 600]}
    v = Validator(simple_dict_schema, allow_list_missing=True)
    assert (v.validate(document) is True)
    assert (v.errors == {})


# ----------------------------------------------------------------------------------------------------------------------

def test_extended_list_validation_works():
    document = [
        ['test1', 501, ['test2', 1, 2, 55]],
        600,
        ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ['test10', 600, 'test11']
    ]
    v = Validator(extended_list_schema)
    assert (v.validate(document) is True)
    assert (v.errors == {})


def test_extended_list_validation_breaks():
    document = [
        ['test1', 501, ['test', 1, 2, 'testwrongtype']],
        600,
        ['test3', 1, 2, {'field3': 'testfield', 'field2': 5}],
        ['test10', 600, 'test11']
    ]
    v = Validator(extended_list_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'_schema': [
        {0: [{2: [{3: ['must be of integer type']}]}], 2: [{3: [{'field3': ['unknown field']}]}]}
    ]})


def test_extended_list_validation_min_number_not_compliant():
    document = [
        ['test1', 499, ['test2', 1, 2, 55]],
        600,
        ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ['test10', 600, 'test11']
    ]
    v = Validator(extended_list_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'_schema': [{0: [{1: ['min value is 500']}]}]})


def test_extended_list_validation_list_len_breaks():
    document = [
        ['test1', 501, ['test2', 1, 2, 55]],
        600,
        ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ['test10', 600]
    ]
    v = Validator(extended_list_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'_schema': [{3: ['length of list should be 3, it is 2']}]})


def test_extended_list_validation_list_len_works():
    document = [
        ['test1', 501, ['test2', 1, 2, 55]],
        600,
        ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ['test10', 600]
    ]
    v = Validator(extended_list_schema, allow_list_missing=True)
    assert (v.validate(document) is True)
    assert (v.errors == {})


# ----------------------------------------------------------------------------------------------------------------------

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
    print(v.errors)
    assert (v.validate(document) is True)
    assert (v.errors == {})


def test_extended_dict_validation_breaks():
    document = {
        'list_of_values': [
            'test1',
            600,
            ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 501, '3': ['test2', 1, 2, 55, 'hello']},
        'list_of_values_3': ['test10', 600, 'test11']
    }
    v = Validator(extended_dict_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'list_of_values_2': [{'3': ['length of list should be 4, it is 5']}]})


def test_extended_dict_validation_min_number_not_compliant():
    document = {
        'list_of_values': [
            'test1',
            600,
            ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 499, '3': ['test2', 1, 2, 55, 'hello']},
        'list_of_values_3': ['test10', 600, 'test11']
    }
    v = Validator(extended_dict_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'list_of_values_2': [{'2': ['min value is 500'], '3': ['length of list should be 4, it is 5']}]})


def test_extended_dict_validation_list_len_breaks():
    document = {
        'list_of_values': [
            'test1',
            600,
            ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 501, '3': ['test2', 1, 2]},
        'list_of_values_3': ['test10', 600, 'test11']
    }
    v = Validator(extended_dict_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'list_of_values_2': [{'3': ['length of list should be 4, it is 3']}]})


def test_extended_dict_validation_list_len_works():
    document = {
        'list_of_values': [
            'test1',
            600,
            ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 501, '3': ['test2', 1, 2]},
        'list_of_values_3': ['test10', 600, 'test11']
    }
    v = Validator(extended_dict_schema, allow_list_missing=True)
    assert (v.validate(document) is True)
    assert (v.errors == {})


# ----------------------------------------------------------------------------------------------------------------------

def test_extended_list_validation_too_many_fields_raise():
    document = [
        ['test1', 501, ['test2', 1, 2, 55]],
        600,
        ['test3', 1, 2, {'field1': 'testfield', 'field2': 5, 'field3': 4}],
        ['test10', 600]
    ]
    v = Validator(extended_list_schema)
    assert (v.validate(document) is False)
    assert (v.errors == {'_schema': [{2: [{3: [{'field3': ['unknown field']}]}], 3: ['length of list should be 3, it is 2']}]})


def test_extended_dict_validation_too_many_fields_raise():
    document = {
        'list_of_values': [
            'test1',
            600,
            ['test3', 1, 2, {'field1': 'testfield', 'field2': 5}],
        ],
        'list_of_values_2': {'1': 'test1', '2': 501, '3': ['test2', 1, 2, 55, 'hello']},
        'list_of_values_3': ['test10', 600, 'test11']
    }
    v = Validator(extended_dict_schema, allow_list_missing=True)
    assert (v.validate(document) is False)
    assert (v.errors == {'list_of_values_2': [{'3': [{4: ['unknown field']}]}]})


"""
if __name__ == '__main__':


    document = {
        'list_of_values': ['rawr', 1000, ['sfsdf', 1, 4, {'field1': 'dasdsa', 'field2': 3, 'field3': 'sfd'}]],
        'list_of_values_2': ['fd', 1000, ['sfsdf', 1, 5434, 4, 4]],
    }

    v = Validator(schema, allow_list_missing=True)

    print(1, v.validate(document), v.errors)
    print(1, v.validate(document, schema), v.errors)

    print(2, v.normalized(document))
    print(2, v.normalized(document, schema))

    print(3, v.normalized_as_dict(document, schema))
    print(3, v.normalized_as_dict(document))

    print(1, v.validate(document), v.errors)
    print(1, v.validate(document, schema), v.errors)

    print(2, v.normalized(document))
    print(2, v.normalized(document, schema))

    print(3, v.normalized_as_dict(document, schema))
    print(3, v.normalized_as_dict(document))

    a = v.normalized_as_object(document)
    b = v.normalized_as_object(document, schema)
    print(4, a.hello[2].hi)
    print(4, b.hello[2].hi)

    print(help(v))

"""
