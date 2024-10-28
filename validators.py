from . import USSDValidationError
import re
def validate_int(val: str):
    try:
        return int(str)
    except:
        raise USSDValidationError('invalid integer conversion')
def validate_email(val: str):
    test = re.fullmatch('', val)
    if test == False:
        raise USSDValidationError('invalid email')
    return val
def validate_max(val: str):
    test = re.fullmatch('', val)
    if test == False:
        raise USSDValidationError('invalid email')
    return val

def validate_min(val: str):
    ...

def validate_max_length(val: str):
    ...

def validate_min_length(val: str):
    ...