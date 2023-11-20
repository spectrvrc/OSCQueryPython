from enum import IntEnum
from typing import Dict, Type

class AccessValues(IntEnum):
    NoValue = 0
    ReadOnly = 1
    WriteOnly = 2
    ReadWrite = 3
        

_osc_type_lookup: Dict[Type, str] = {
    int: "i",
    float: "f",
    str: "s",
    bytes: "b",
    bool: "T"
}

def osc_type_for(python_type: Type) -> str:
    """
    Get the OSC type string for a given Python type.
    """
    return _osc_type_lookup.get(python_type, "")