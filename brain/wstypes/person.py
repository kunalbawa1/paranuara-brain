from wstypes import TypeBase

class WSPerson(TypeBase):
    def __init__(self, **kwargs):
        self._base_type = 'Person'
        TypeBase.__init__(self, **kwargs)
        self._attribute('username', kwargs)
        self._attribute('died', kwargs)
        self._attribute('balance', kwargs)
        self._attribute('picture', kwargs)
        self._attribute('age', kwargs)
        self._attribute('eye_color', kwargs)
        self._attribute('name', kwargs)
        self._attribute('gender', kwargs)
        self._attribute('email', kwargs)
        self._attribute('phone', kwargs)
        self._attribute('address', kwargs)
        self._attribute('description', kwargs)
        self._attribute('registered_date', kwargs)
        self._attribute('tags', kwargs)
        self._attribute('fruits', kwargs)
        self._attribute('vegetables', kwargs)
        self._attribute('company', kwargs)

