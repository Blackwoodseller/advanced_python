"""Homework metaclass with property generator"""

from collections import defaultdict
import re
import types


class PropertySetter(type):
    """Property generator metaclass"""

    def __new__(cls, name, bases, classdict):
        """Overrided __new__ method for properties creation"""

        print('name: {}'.format(name))
        print('Initial_classdict: {}'.format(classdict))

        props = defaultdict(dict)
        action_pattern = '^(set|get|del)_'
        for name, item in classdict.items():
            if isinstance(item, types.FunctionType):
                res = re.search(action_pattern, name)
                if res:
                    props[name[4:]][res.group(1)] = item

        for prop, funcs in props.items():
            if prop not in classdict:
                classdict[prop] = property(fset=funcs.get('set'),
                                           fget=funcs.get('get'),
                                           fdel=funcs.get('del'))

        print('Updated classdict: {}'.format(classdict))
        return type.__new__(cls, name, bases, classdict)


class Example(metaclass=PropertySetter):
    """Property test class"""
    def __init__(self):
        self._x = None

    def get_x(self):
        """x getter"""
        return self._x

    def set_x(self, value):
        """x setter"""
        self._x = value

    def get_y(self):
        """y getter"""
        return 'y'


ex = Example()
ex.x = 255
print(ex.x)
print(ex.y)
