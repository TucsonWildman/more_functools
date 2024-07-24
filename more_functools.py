'''
More Func Tools!

An extension of the `functools` module from the standard library.
'''
from abc        import ABC, abstractmethod
from functools  import *
from typing     import Any, Callable, Union

__all__ = ['readonly', 'class_property', 'cached_class_property', 'lru_staticmethod', 'lru_classmethod']

def readonly(ABC):
    '''
    All attributes of a readonly instance
    cannot be changed once set.
    '''
    def __setattr__(self, k, v):
        if not hasattr(self, k): super().__setattr__(k, v)
    #End-def
#End-def

class _method_wrap(ABC):
    def __init__(self, func : Callable): self.func = func
#End-class

class class_property(_method_wrap, readonly):
    '''
    Same as the built-in `property` but for the class.
    
    Use the same convention as defining a `classmethod`
    '''
    def __getattr__(self, k): return getattr(self.func, k, None)
    
    @staticmethod
    def decide_owner(instance, owner):
        if owner == None: owner = getattr(instance, '__class__', None)
        return owner
    #End-def`
    
    def __get__(self, instance, owner=None): return self.func(self.decide_owner(instance, owner) )
#End-class

class cached_class_property(cached_property, class_property):
    '''
    Cached property for a class.
    
    Useful in cases where such properties are, in the very least, most easily calculated post-class-definition.
    '''
    def __get__(self, instance, owner=None): return super().__get__(self.decide_owner(instance, owner) )
#End-class