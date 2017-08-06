from wstypes import TypeBase

class Error(TypeBase):
    def __init__(self, **kwargs):
        TypeBase.__init__(self, **kwargs)
        # set class name
        self._class_name = 'Error'
        self._base_type = 'Error'

        # default error
        self.name = self.__class__.__name__
        if 'name' in kwargs:
            self.name = kwargs['name']
        self.code = -1000
        self._attribute('id', kwargs)
        self._attribute('name', kwargs)
        self._attribute('code', kwargs)
        self._attribute('description', kwargs)
        self._attribute('message', kwargs)

class NoResultsError(Error):
    def __init__(self, **kwargs):
        Error.__init__(
            self,
            description='No results found for service call.',
            code=-1101,
            **kwargs)