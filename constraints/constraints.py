__author__ = 'orish_000'

from collections import namedtuple
from severity import CONSTRAINT_SEVERITY_TYPES

Constraint = namedtuple("Constraint", ["condition", "severity"])


def create_person_constraint(person, severity):
    assert severity in CONSTRAINT_SEVERITY_TYPES
    return Constraint(condition=lambda p: p != person, severity=severity)