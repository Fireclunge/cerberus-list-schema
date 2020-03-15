simple_list_schema = {
    'type': 'list',
    'name': 'hello',
    'items': [
        {'type': 'string'},
        {'type': 'integer', 'min': 500},
        {'type': 'string'},
    ]
}

# --------------------

other_schema = {
    'type': 'list',
    'items': [
        {'type': 'string'},
        {'type': 'integer', 'min': 500},
        {'type': 'list',
         'items': [
             {'type': 'string'},
             {'type': 'integer', 'name': 'second_int'},
             {'type': 'integer'},
             {'type': 'integer', 'min': 50},
         ]
         }
    ]
}

extended_list_schema = {
    'type': 'list',
    'name': 'hello',
    'items': [
        other_schema,
        {'type': 'integer', 'min': 500},
        {'type': 'list',
         'items': [
             {'type': 'string'},
             {'type': 'integer'},
             {'type': 'integer', 'name': 'hi'},
             {'type': 'dict',
              'schema': {
                  'field1': {'type': 'string', 'name': 'field01231'},
                  'field2': {'type': 'integer'}}}
         ]
         },
        simple_list_schema
    ]
}
