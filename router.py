from typing import Callable, Dict
import re
class Radix:
    def __init__(self, **kwargs):
        self.children: Dict[str, 'Radix'] = {}
        self.is_terminal = False
        self.value = None
        self.handlers: Callable | None = None
        self.alias = kwargs.get('alias', None)
        self.validator = None
    def insert(self, route, func):
        node = self
        tokens = [i for i in route.split('*') if i]
        for token in tokens:     
            match = re.match(r'\{([^}]+)\}', token)
            if match:
                token = '*' 
            if not node.children.get(token, False):
                node.children[token] = Radix()
                if token == "*":
                    t = match.group(1).split()
                    key = t[0]
                    node.children[token].alias = key
                    if len(t) > 1:
                        match t[1]:
                            case "int":
                                self.validator = int
                            case "str":
                                self.validator = str
                            
            node = node.children[token]
        node.is_terminal = True
        node.handlers = func
    def find(self, route, **kwargs):
        node = self
        tokens = [i for i in route.split('*') if i]
        for token in tokens:
            if node.children.get(token, None) == None:
                if '*' in node.children:
                    node = node.children["*"]
                    params = kwargs.get('params', {})
                    params[node.alias] = self.validator(token) if self.validator else token
                    continue
                else:
                    return None
            node = node.children[token] 
        func = node.handlers    
        return func
    
class Router:
    def __init__(self):
        self.tree = Radix()
    def add_route(self, route: Callable):
        def wrapper(fn):
            def inner(*args, **kwargs):
                self.tree.insert(route, fn)        
            inner()
        return wrapper
    def include_router(self, router: "Router", path= ""):        
        if path in self.tree.children:
            raise IndexError("Path already exists")
        for key, child in router.tree.children.items():
            self.tree.children[key] = child
        
    def get_handler(self, route, **kwargs):
        return self.tree.find(route, **kwargs)