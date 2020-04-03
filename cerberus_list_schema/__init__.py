from copy import deepcopy

from cerberus import Validator as CerberusValidator, errors
from cerberus.schema import DefinitionSchema
from munch import DefaultMunch


class DummyClass:
    pass


class Validator(CerberusValidator):
    _is_list_schema = None
    _allow_name_conflicts = None
    _callable_numbers = None

    @staticmethod
    def _parse_list_document(document):
        if isinstance(document, list):
            return {"_schema": document}
        else:
            return document

    def _check_for_list_schema(self, schema):
        if schema.get("type") == "list":
            schema = {"_schema": schema}
            self._is_list_schema = True
            return schema
        else:
            self._is_list_schema = False
            return schema

    def _parse_schema_in_args(self, args):
        args_parse = list(args)
        schema = args_parse[0]
        schema = self._check_for_list_schema(schema)
        if self._is_list_schema:
            args_parse[0] = schema
            return tuple(args_parse)
        else:
            return args

    def _iterate_list_for_rename(self, array, current_schema):
        def _validate_valid_name_rule(new_name):
            # to test of setattr can work converting dicts to objects. is 'name' rule valid
            dummy = DummyClass
            setattr(dummy, new_name, "test_value")
            try:
                int(str(new_name)[0])
            except ValueError:
                pass
            except IndexError:
                if str(new_name).strip() == "":
                    raise ValueError(
                        "`name` rule (`{0}`) in provided schema is not valid as it is blank. "
                        "Make sure it is a valid name for a python variable.".format(
                            new_name
                        )
                    )
            else:
                raise ValueError(
                    "`name` rule (`{0}`) in provided schema is not valid as it begins with a number. "
                    "Make sure it is a valid name for a python variable.".format(
                        new_name
                    )
                )

            try:
                eval("dummy.{0}".format(new_name))
            except SyntaxError:
                raise ValueError(
                    "`name` rule (`{0}`) in provided schema is not valid. "
                    "Make sure it is a valid name for a python variable.".format(
                        new_name
                    )
                )

        def _get_node_schema(k):
            if isinstance(array, dict):
                return current_schema["schema"].get(k, {})
            elif isinstance(array, list):
                try:
                    return current_schema["items"][k]
                except (IndexError, KeyError):
                    return {}

        def _replace_values(k, v, allow_name_conflicts=False, callable_numbers=False):
            if isinstance(v, dict) or isinstance(v, list):
                v = self._iterate_list_for_rename(v, new_schema)
            new_name = new_schema.get("name")
            if new_name is not None:
                _validate_valid_name_rule(new_name)
                if new_dict.get(new_name) is not None and allow_name_conflicts is False:
                    raise AttributeError(
                        "`name` rule (`{0}`) already in use by another field".format(
                            new_name
                        )
                    )
                else:
                    new_dict[new_name] = v
                indexes_to_pop.append(k)
            else:
                if callable_numbers is True:
                    if isinstance(k, int) or isinstance(k, float):
                        k = "_{k}".format(k=k)
                    try:
                        _validate_valid_name_rule(k)
                    except ValueError:
                        k = "_{k}".format(k=k)
                new_dict[k] = v

        new_dict = dict()
        indexes_to_pop = list()

        if isinstance(array, list):
            for key, value in enumerate(array):
                new_schema = _get_node_schema(key)
                _replace_values(
                    key, value, self._allow_name_conflicts, self._callable_numbers
                )

            indexes_to_pop.sort(reverse=True)
            for index in indexes_to_pop:
                del array[index]

        elif isinstance(array, dict):
            for key, value in array.items():
                new_schema = _get_node_schema(key)
                _replace_values(
                    key, value, self._allow_name_conflicts, self._callable_numbers
                )

            for key in indexes_to_pop:
                del array[key]

        return new_dict

    def _validate_items(self, items, field, values):
        """ {'type': 'list', 'check_with': 'items'} """

        if len(items) != len(values) and not self.allow_list_missing:
            self._error(field, errors.ITEMS_LENGTH, len(items), len(values))
        else:
            schema = dict(
                (i, definition) for i, definition in enumerate(items)
            )  # noqa: E501
            validator = self._get_child_validator(
                document_crumb=field,
                schema_crumb=(field, "items"),  # noqa: E501
                schema=schema,
            )
            if not validator(
                dict((i, value) for i, value in enumerate(values)),
                update=self.update,
                normalize=False,
            ):
                self._error(field, errors.BAD_ITEMS, validator._errors)

    def __init_processing(self, document, schema=None):
        if schema is not None:
            schema = self._check_for_list_schema(schema)
        if self._is_list_schema:
            document = self._parse_list_document(document)
        super(Validator, self)._BareValidator__init_processing(document, schema)

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self._original_schema = deepcopy(args[0])
            args = self._parse_schema_in_args(args)

        super(Validator, self).__init__(*args, **kwargs)
        self.allow_list_missing = kwargs.get("allow_list_missing", False)

    def _validate_name(self, items, field, values):
        """ Test the oddity of a value.

        The rule's arguments are validated against this schema:
        {'type': 'string'}
        """
        pass

    def validate(self, document, schema=None, update=False, normalize=True):
        if schema is not None:
            schema = self._check_for_list_schema(schema)
        else:
            schema = self._schema
        if self._is_list_schema:
            document = self._parse_list_document(document)
            if isinstance(schema, DefinitionSchema):
                if (
                    len(schema.schema["_schema"]["items"]) != len(document["_schema"])
                ) and self.allow_list_missing:
                    schema_items = schema.schema["_schema"]["items"]
                    schema_items = schema_items[0 : len(document["_schema"])]
                    schema.schema["_schema"]["items"] = schema_items
        return super(Validator, self).validate(document, schema, update, normalize)

    def normalized(self, document, schema=None, always_return_document=False):

        if schema is not None:
            schema = self._check_for_list_schema(schema)
        else:
            schema = self._schema
        if self._is_list_schema:
            document = self._parse_list_document(document)
            return super(Validator, self).normalized(
                document, schema, always_return_document
            )["_schema"]
        else:
            return super(Validator, self).normalized(
                document, schema, always_return_document
            )

    def normalized_as_dict(
        self,
        document,
        schema=None,
        always_return_document=False,
        allow_name_conflicts=False,
        callable_numbers=False,
    ):
        """ Returns normalized() dictionary but converts list objects to dict schema

        See normalized method doctring for more information such as expected parameters

        :param allow_name_conflicts: Set to True to allow dictionary keys to be overwriten by already existing keys
               when using the `name` rule. If set to False and exception will be raised.
        :type allow_name_conflicts: :class:`bool`
        """

        normalized_document = deepcopy(
            self.normalized(document, schema, always_return_document)
        )
        if schema is None:
            try:
                schema = self._original_schema
            except AttributeError:
                raise AttributeError("Schema not found. Perhaps it wasn't loaded.")
        if isinstance(document, dict):
            schema = {"schema": schema}
        self._allow_name_conflicts = allow_name_conflicts
        self._callable_numbers = callable_numbers
        return self._iterate_list_for_rename(normalized_document, schema)

    def normalized_as_object(
        self,
        document,
        schema=None,
        always_return_document=False,
        allow_name_conflicts=False,
        callable_numbers=False,
    ):
        """ Returns normalized_as_dict() as an object with keys callable.

        See normalized method doctring for more information such as expected parameters
        """
        return DefaultMunch.fromDict(
            self.normalized_as_dict(
                document,
                schema,
                always_return_document,
                allow_name_conflicts,
                callable_numbers,
            )
        )
