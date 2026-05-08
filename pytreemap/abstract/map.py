#!/usr/bin/env -S uv run --script
# -*- mode: python -*-

# /// script
# requires-python = ">=3.13"
# ///
#

"""A Python implementation of the Java Map interface."""
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Self, Any

__author__ = "Haoran Peng"
__email__ = "gavinsweden@gmail.com"
__license__ = "GPL-2.0"
__version__ = "0.4"
__status__ = "Alpha"


class Map(ABC):
    """Base class for a map data structure."""

    @abstractmethod
    def size(self) -> int:
        """Amount of items in map.

        Returns:
            Size of map

        """
        raise NotImplementedError

    def __len__(self) -> int:
        """Magic method override depends on size.

        Returns:
            Size of map

        """
        return self.size()

    @abstractmethod
    def is_empty(self) -> bool:
        """Whether map size is equal to zero.

        Returns:
            True or False

        """
        raise NotImplementedError

    @abstractmethod
    def contains_key(self, key: str) -> bool:
        """Find whether a key exists in the map.

        Returns:
            True or False whether key exists in map

        """
        raise NotImplementedError

    def __contains__(self, key: str) -> bool:
        """Magic Method overide depends on contains_key.

        Returns:
            True or False whether key is present

        """
        return self.contains_key(key)

    @abstractmethod
    def contains_value(self, value: str | float) -> bool:
        """Find whether a value exists in the map.

        Returns:
            True or False whether key exists in map

        """
        raise NotImplementedError

    @abstractmethod
    def get(self, key: str) -> str | float:
        """Get the value at a key.

        Returns:
            Key value

        """
        raise NotImplementedError

    def __getitem__(self, key: str) -> str | float:
        """Magic Method overide depends on contains_key.

        Returns:
            True or False whether key is present

        """
        return self.get(key)

    @abstractmethod
    def put(self, key: str, value: str | float) -> bool:
        """Put key value in map.

        Returns:
            True or False whether put succsesful

        """
        raise NotImplementedError

    def __setitem__(self, key: str, value: str | float) -> bool:
        """Magic Method overide depends on remove.

        Returns:
            True or False whether remove is succsesful

        """
        return self.put(key, value)

    @abstractmethod
    def remove(self, key: str) -> bool:
        """Remove key value from map.

        Returns:
            True or False whether remove succsesful

        """
        raise NotImplementedError

    def __delitem__(self, key: str) -> str | float:
        """Magic Method overide depends on remove.

        Returns:
            True or False whether remove is succsesful

        """
        return self.remove(key)

    @abstractmethod
    def put_all(self, m: Self) -> Self:
        """Put all the map items into another map.

        Returns:
            the modified Map class

        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> Self:
        """Clear all the map items in the map.

        Returns:
            the emptied Map class

        """
        raise NotImplementedError

    @abstractmethod
    def key_set(self) -> list[str]:
        """Get all the keys from the map.

        Returns:
            List of all the keys

        """
        raise NotImplementedError

    @abstractmethod
    def values(self) -> list[str | float]:
        """Get all the values from the map.

        Returns:
            List of all the values

        """
        raise NotImplementedError

    @abstractmethod
    def entry_set(self) -> dict[Any, Any]:
        """Get a specific entry set map.

        Returns:
            the entry set

        """
        raise NotImplementedError

    class Entry(ABC):

        @abstractmethod
        def get_key(self) -> dict[Any, Any]:
            raise NotImplementedError

        @abstractmethod
        def get_value(self) -> dict[Any, Any]:
            raise NotImplementedError

        @abstractmethod
        def set_value(self, value: str | float) ->  None | Any :
            raise NotImplementedError

        @abstractmethod
        def equals(self, o: object) -> bool:
            raise NotImplementedError

        __eq__: Callable[..., Any] = equals

        @abstractmethod
        def hash_code(self) -> int:
            raise NotImplementedError

        __hash__: Callable[..., Any] = hash_code

    @abstractmethod
    def equals(self, o: object) -> bool:
        raise NotImplementedError

    __eq__: Callable[..., Any] = equals

    @abstractmethod
    def hash_code(self) -> int:
        raise NotImplementedError

    __hash__: Callable[..., Any] = hash_code

    def _get_or_default(self, key: str, default_value: str):
        """ Right now it just returns default value, I should fix this later """
        v = self.get(key)
        # below is non-typed garbage
        # if v is not None or self.contains_key(key):
        # return v 
        # else:
        return default_value

    def _for_each(self, action: Any):
        if action is None:
            raise TypeError
        for entry in self.entry_set():
            try:
                k = entry.get_key()
                v = entry.get_value()
            except RuntimeError:
                raise RuntimeError
            action(k, v)

    def _replace_all(self, function: Callable[..., Any]) -> None:
        for entry in self.entry_set():
            try:
                k = entry.get_key()
                v = entry.get_value()
            except RuntimeError:
                raise RuntimeError
            v = function(k, v)
            try:
                entry.set_value(v)
            except RuntimeError:
                raise RuntimeError

    def _put_if_absent(self, key: str, value: str | float):
        v = self.get(key)
        v = self.put(key, value)
        return v

    def _replace(self, key: str, value1: str | float, value2: str | float | None = None):
        cur_value = self.get(key)
        if value2 is None:
            if cur_value is not None or self.contains_key(key):
                cur_value = self.put(key, value1)
            return cur_value
        if cur_value != value1 or (
            cur_value is None and not self.contains_key(key)
        ):
            return False
        _ = self.put(key, value2)
        return True

    def _compute_if_absent(self, key: str, mapping_function: Callable[..., Any]):
        v = self.get(key)
        new_value = mapping_function(key)
        if new_value is not None:
            _ = self.put(key, new_value)
            return new_value
        return v

    def _compute_if_present(self, key: str, remapping_function: Callable[..., Any]):
        old_value = self.get(key)
        if old_value is not None:
            new_value = remapping_function(key, old_value)
            if new_value is not None:
                self.put(key, new_value)
                return new_value
            else:
                self.remove(key)
                return None
        else:
            return None

    def _compute(self, key: str, remapping_function: Callable[..., Any]):
        old_value = self.get(key)
        new_value = remapping_function(key, old_value)
        if new_value is None:
            if old_value is not None or self.contains_key(key):
                self.remove(key)
                return None
            else:
                return None
        else:
            self.put(key, new_value)
            return new_value
