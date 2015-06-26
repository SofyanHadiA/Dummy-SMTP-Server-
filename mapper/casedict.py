# Copyright (c) 2013 Optiflows
# https://bitbucket.org/optiflowsrd/obelus/src/tip/obelus/casedict.py

from collections import MutableMapping


_sentinel = object()


class CaseDict(MutableMapping):
    """
    A case-insensitive dictionary.
    """

    __slots__ = ('_data',)

    def __init__(self, __dict=None, **kwargs):
        # lower-cased => (original casing, value)
        self._data = {}
        if __dict is not None:
            self.update(__dict)
        if kwargs:
            self.update(kwargs)

    # Minimum set of methods required for MutableMapping

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return (v[0] for v in self._data.values())

    def __getitem__(self, key):
        return self._data[key.lower()][1]

    def __setitem__(self, key, value):
        self._data[key.lower()] = (key, value)

    def __delitem__(self, key):
        del self._data[key.lower()]

    # Methods overriden to mitigate the performance overhead.

    def __contains__(self, key):
        return key.lower() in self._data

    def clear(self):
        self._data.clear()

    def get(self, key, default=_sentinel):
        tup = self._data.get(key.lower())
        if tup is not None:
            return tup[1]
        elif default is not _sentinel:
            return default
        else:
            return None

    def pop(self, key, default=_sentinel):
        if default is not _sentinel:
            tup = self._data.pop(key.lower(), default)
        else:
            tup = self._data.pop(key.lower())
        if tup is not default:
            return tup[1]
        else:
            return default

    # Other methods

    def __repr__(self):
        if self._data:
            return '%s(%r)' % (self.__class__.__name__, dict(self))
        else:
            return '%s()' % self.__class__.__name__
