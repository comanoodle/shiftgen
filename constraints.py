__author__ = 'orish_000'

from collections import namedtuple
from consts import CONSTRAINT_SEVERITIES

Constraint = namedtuple("Constraint", ["constraint_func", "severity"])

def create_person_constraint(person, level):
    assert level in CONSTRAINT_SEVERITIES
    return Constraint(constraint_func=lambda p: p != person, severity=level)