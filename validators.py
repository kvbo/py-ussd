from . import USSDValidationError
import re
def validate_int(val: str):
    try:
        return int(val)
    except:
        raise USSDValidationError('invalid integer conversion')
def validate_email(val: str):
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', val)
    if valid == False:
        raise USSDValidationError('invalid email')
    return val

def validate_max(val, max):
    if val > int(max):
        raise USSDValidationError(f'input shoudn\'t be greater than {max}')
    return val

def validate_min(val, min):
    if val < int(min):
        raise USSDValidationError(f'input shoudn\'t be less than {min}')
    return val

def validate_max_length(val: str, max: int):
    if len(val) > int(max):
        raise USSDValidationError(f'input should not be more than {max} in length')
    return val   
 
def validate_min_length(val: str, min: int):
    if len(val) < int(min):
        raise USSDValidationError(f'input should not be less than {min} in length')
    return val 