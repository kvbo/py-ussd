from .router import Router
from .errors import USSDRouteDoesNotExit
class USSD(Router):
    _instance = None
    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = super(USSD, cls).__new__(cls)
        return cls._instance
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.middlewares = []
    def use(self, middleware, config=None) -> None:
        self.middlewares.append(middleware)
    def handler(self, path="", params={}):
        fn = self.get_handler(path, params=params)
        if fn == None:
            raise USSDRouteDoesNotExit("not found")
        return fn(params)

            
            