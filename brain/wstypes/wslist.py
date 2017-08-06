from wstypes import TypeBase

class List(TypeBase):

    def __init__(self, **kwargs):
        self._base_type = 'List'
        TypeBase.__init__(self, **kwargs)
        self._attribute('description', kwargs)
        self._attribute('items', kwargs)
        self._attribute('total', kwargs)

    def reverse(self):
        self.items.reverse()

    def __len__(self):
        try:
            return len(self.items)
        except:
            return 0
