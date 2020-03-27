from copy import deepcopy

from cerberus_list_schema.tests.test_data.dict_schemas import (
    simple_dict_schema,
    extended_dict_schema,
)
from cerberus_list_schema.tests.test_data.list_schemas import (
    simple_list_schema,
    extended_list_schema,
)
from cerberus_list_schema.tests.test_data.multiuse_schema import schema


def get_simple_list_schema():
    return deepcopy(simple_list_schema)


def get_simple_dict_schema():
    return deepcopy(simple_dict_schema)


def get_extended_list_schema():
    return deepcopy(extended_list_schema)


def get_extended_dict_schema():
    return deepcopy(extended_dict_schema)


def get_multiuse_schema():
    return deepcopy(schema)
