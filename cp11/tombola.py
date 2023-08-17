import abc


class Tombola(abc.ABC):

    @abc.abstractmethod
    def load(self, iterable):
        """add elements from iterable"""
    
    @abc.abstractmethod
    def pick(self):
        """
        Randomly delete element, and return it.
        If it is None, throw LookupError
        """
    
    def loaded(self):
        return bool(self.inspect())
    
    def inspect(self):
        """Return an ordered tuple, constructed by current elements"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))

