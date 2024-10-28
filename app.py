from .router import Router
from .errors import USSDRouteDoesNotExit
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
class USSD(Router):
    _instance = None
    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = super(USSD, cls).__new__(cls)
        return cls._instance
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.middlewares = []
        self.validatiors = {}
    def use(self, middleware, config=None) -> None:
        self.middlewares.append(middleware)
    def register_validators(self, key, func):
        self.validatiors[key] = func
        
    def handler(self, path="", params={}):
        logging.debug(path)
        fn = self.get_handler(path, params=params)
        if fn == None:
            raise USSDRouteDoesNotExit
        return fn(params)

            
            