class TypeBase(object):
    """
    Base class for all WS types.
    """

    def __init__(self, **kwargs):
        # default error
        if 'name' in kwargs:
            self.name = kwargs['name']

        if 'base_type' in kwargs:
            if self._base_type in ('', None):
                self._base_type = kwargs['base_type']

    def _attribute(self, name, args, default=None):
        if not isinstance(name, basestring):
            raise Exception('Attribute name must be a string.')
        if name not in args:
            return
        if args[name] is None:
            if default is not None:
                self.__dict__[name] = default
            return
        self.__dict__[name] = args[name]

    def to_json(self):
        json_resp = {}
        json_resp[self._base_type] = {}
        for key, value in self.__dict__.iteritems():
            if key.startswith('_'):
                continue
            if value is None:
                continue
            # If list then attempt to convert each item in list to json
            if isinstance(value, list):
                json_values = []
                for v in value:
                    if isinstance(v, TypeBase):
                        json_values.append(v.to_json())
                if json_values:
                    value = json_values

            json_resp[self._base_type][key] = value
        return json_resp
