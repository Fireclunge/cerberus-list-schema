other_schema = {
    'type': 'list',
    'items': [
        {'type': 'string'},
        {'type': 'integer', 'min': 500},
        {'type': 'list',
         'items': [
             {'type': 'string'},
             {'type': 'integer', 'name': 'nd_int'},
             {'type': 'integer'},
             {'type': 'integer', 'min': 50},
         ]
         }
    ]
}

schema = {
    'list_of_values': {
        'type': 'list',
        'name': 'hello',
        'items': [
            {'type': 'string'},
            {'type': 'integer', 'min': 500},
            {'type': 'list',
             'items': [
                 {'type': 'string'},
                 {'type': 'integer'},
                 {'type': 'integer', 'name': 'hi'},
                 {'type': 'dict', 'schema': {'field1': {'type': 'string', 'name': 'field01231'}, 'field2': {'type': 'integer'}}}
             ]
             }
        ]
    },
    'list_of_values_2': other_schema
}
