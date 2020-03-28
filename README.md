[![PyPI version](https://badge.fury.io/py/cerberus-list-schema.svg)](https://badge.fury.io/py/cerberus-list-schema)
[![Build Status](https://travis-ci.org/Fireclunge/cerberus-list-schema.svg?branch=master)](https://travis-ci.org/Fireclunge/cerberus-list-schema)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Cerberus List Schema** is a **Cerberus based validation library with extended methods** to support list schemas as well 
as list transposition to dictionary and python objects. 

- List/array schema support
- Transposition of lists to python objects via schemas
- Support for missing values in document

## Installation

Cerberus List Schema can be installed using pip.

```
$ pip install cerberus-list-schema
```

## Extensions
### Validation

```python
>>> schema = {
>>>     "type": "list",
>>>     "items": [{"type": "string"}, {"type": "integer", "min": 20}],
>>> }
```

##### Simple validation

Lists can now be validated out of context of a dictionary

```python
>>> document = ["Apples", 40]
>>> v = Validator(schema)
>>> v.validate(document)
True
```

... and usual cerberus validation rules still apply

```python
>>> document = ["Apples", 15]
>>> v.validate(document)
False
>>> v.errors
{'_schema': [{1: ['min value is 20']}]}
```

##### Allow incomplete documents

In cerberus, documents that are missing information specified in a list schema will fail. 
Using Cerberus List Schema you can pass `allow_list_missing=True` to a Validator object to enable incomplete lists.

```python
>>> document = ["Apples"]
>>> v.validate(document)
False
>>> v.errors
{'_schema': ['length of list should be 2, it is 1']}

>>> v = Validator(schema, allow_list_missing=True)
>>> v.validate(document)
True
```

### Normalization

##### Normalization as dict

Lists can now be normalized as dict additional to the standard cerberus validation. 
By default they are given a key equalled to their list index.

```python
>>> document = {"produce": ["Apple", 5, "High"]}
>>> schema = {
>>>     "produce": {
>>>         "type": "list",
>>>         "items": [
>>>             {"type": "string"},
>>>             {"type": "integer", "min": 0},
>>>             {"type": "string"},
>>>         ],
>>>     }
>>> }
>>> v = Validator(schema)
>>> v.normalized_as_dict(document)
{"fruits": {0: "Apple", 1: 5, 2: "High"}}
```

However by using the `name` rule, lists can be assigned to a namable dict. Note that this is different to `rename`
and should be preferred when using the dictionary normalization as rename can produce adverse effects.

```python
>>> document = {"produce": ["Apple", 5, "High"]}
>>> schema = {
>>>     "produce": {
>>>         "type": "list",
>>>         "name": "fruits",
>>>         "items": [
>>>             {"name": "type", "type": "string"},
>>>             {"name": "count", "type": "integer", "min": 0},
>>>             {"name": "quality", "type": "string"},
>>>         ],
>>>     }
>>> }
>>> v = Validator(schema)
>>> v.normalized_as_dict(document)
{'fruits': {'type': 'Apple', 'count': 5, 'quality': 'High'}}
```

By default, conflicting names will throw an error. 
However, `allow_name_conflicts` can be specified to ignore the error. 
In this case, previous assignments will be overwritten without error

```python
>>> document = {"produce": ["Apple", "Orange"]}
>>> schema = {
>>>     "produce": {
>>>         "type": "list",
>>>         "items": [
>>>             {"name": "fruit_type", "type": "string"},
>>>             {"name": "fruit_type", "type": "string"},
>>>         ],
>>>     }
>>> }
>>> v = Validator(schema)
>>> v.normalized_as_dict(document)
AttributeError: `name` rule (`fruit_type`) already in use by another field
>>> v.normalized_as_dict(document, allow_name_conflicts=True)
{'produce': {'type': 'Orange'}}
```

### Object Mapping

TBC

## Cerberus

More information about Cerberus and its validators can be found in their documentation
 @ https://github.com/pyeve/cerberus

Complete documentation for Cerberus is available at http://docs.python-cerberus.org
