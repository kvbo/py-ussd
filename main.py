from .router import Router
from .errors import USSDRouteDoesNotExit, USSDInternalError

validators = {}
class USSD(Router):
    _instance = None
    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = super(USSD, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, *arg, **kwargs):
        validators = kwargs.get("validators", [])
        del kwargs["validators"]
        
        super().__init__(*arg, **kwargs)
        self.middlewares = []
        self.validators = {}
        
        for validator in validators:
            print(validator)
            self.add_validator(validator)
            
    # def use(self, middleware, config=None) -> None:
    #     self.middlewares.append(middleware)
        
    def handler(self, path="", params={}):
        node = self.get_handler(path, params=params)
        if node == None or node.handler == None:
            raise USSDRouteDoesNotExit("not found")
    
        validators_keys = node.validators
        param = params[node.param]
        for i in validators_keys:
            key, *args = i.split("=")
            func = self.validators[key]
            print(param, key, *args)
            
            param = func(param, *args)
            
        params[node.param] = param
        return node.handler(params)
    

    def add_validator(self, *args):
        if len(args) == 1 and callable(args[0]) and args[0].__name__.startswith("validate_"):
            self.validators[args[0].__name__.split("_", 1)[1]] = args[0]
        elif len(args) == 2 and str(args[0]) and callable(args[1]):
            self.validators[args[0]] = args[1]
        else:
            raise USSDInternalError("error setting up validator")
            

            
            