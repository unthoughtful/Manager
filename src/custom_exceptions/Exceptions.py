'''
Created on 23 Jul 2016

@author: professor
'''

class VariableValueError(Exception):
    """If a class contains an invalid value for a variable.
    """
    pass


class DuplicateRegistrationError(Exception):
    """A Node already has a registration.
    """
    pass
