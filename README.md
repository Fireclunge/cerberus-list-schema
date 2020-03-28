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

##### Naming indexes

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

##### Allowing name conflicts

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

Lists can now be normalized as dict additional to the standard cerberus validation. 
By default they are given a key equalled to their list index. However `name` may be used to rename 
object property to that provided. (ensuring the name is a valid python variable name)

```python
>>> document = {"produce": ["Apple", 5, "High"], "supplier": ["Greg", "United Kingdom", 7.34]}
>>> schema = {
>>>     "produce": {
>>>         "type": "list",
>>>         "name": "fruits",
>>>         "items": [
>>>             {"name": "type", "type": "string"},
>>>             {"name": "count", "type": "integer", "min": 0},
>>>             {"name": "quality", "type": "string"},
>>>         ],
>>>     },
>>>     "supplier": {
>>>         "type": "list",
>>>         "items": [
>>>             {"type": "string"},
>>>             {"type": "string"},
>>>             {"type": "string", "coerce": int},
>>>         ],
>>>     },
>>> }

>>> v = Validator(schema)
>>> obj = v.normalized_as_object(document)

>>> obj.fruits.type  # note produce has been renamed to fruits
'Apple'
>>> obj.fruits.quality
'High'
>>> obj.supplier[0]
'Greg'
>>> obj.supplier[2]  # w/ coerce as int rule applied
7
```

##### Allowing callable properties for unassigned names

Array values without a `name` property can also be callable by using `callable_numbers`. This is places an underscore
before the key index such that it can be called as a property of an object rather than by index.

```python
>>> document = ["Greg", "United Kingdom", 7.34]
>>> schema = {
>>>    "type": "list",
>>>    "items": [
>>>        {"type": "string"},
>>>        {"type": "string", "name": "country"},
>>>        {"type": "string", "coerce": int},
>>>    ],
>>>}

>>> v = Validator(schema)
>>> obj = v.normalized_as_object(document, callable_numbers=True)

>>> obj._0
'Greg'
>>> obj._1  # value renamed to country

>>> obj.country
'United Kingdom'
>>> obj._2
7
```

## Cerberus

More information about Cerberus and its validators can be found on their GitHub page @ https://github.com/pyeve/cerberus

Complete documentation for Cerberus is available at http://docs.python-cerberus.org
