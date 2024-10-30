from typing import Callable, Dict
import re
import time
class Node:
    def __init__(self, **kwargs):
        self.children: Dict[str, 'Node'] = {}
        self.is_terminal = False
        self.value = None
        self.handler: Callable | None = None
        self.param = kwargs.get('param', None)
        self.validators = []
        self.parent: 'Node'| None= None
    def insert(self, route, func):
        node = self
        tokens = [i for i in route.split('*') if i]
        for token in tokens:     
            match = re.match(r'\{([^}]+)\}', token)
            if match:
                token = '*' 
            if not node.children.get(token, False):
                node.children[token] = Node()
                if token == "*":
                    t = match.group(1).split(":")
                    key = t[0]
                    node.children[token].param = key
                    if len(t) > 1:
                        node.children[token].validators.extend(t[1:])
            
            node.children[token].parent = node               
            node = node.children[token]
        node.is_terminal = True
        node.handler = func
        
    def find(self, route, **kwargs) -> 'Node':
        node = self
        tokens = [i for i in route.split('*') if i]
        for token in tokens:
            if node.children.get(token, None) == None:
                if '*' in node.children:
                    node = node.children["*"]
                    params = kwargs.get('params', {})
                    params[node.param] = token
                    continue
                else:
                    return None
            node = node.children[token] 
        
        e = time.perf_counter_ns()
        return node
    
class Router:
    c = 0
    def __init__(self):
        self.tree = Node()
    def route(self, route: Callable):
        def wrapper(fn):
            def inner(*args, **kwargs):
                self.tree.insert(route, fn)        
            inner()
        return wrapper
    def attach_router(self, router: "Router", path= ""):     
        if path in self.tree.children:
            for routeK, v in router.tree.children.items():
                self.tree.children[path].children[routeK] = v
        else:
            self.tree.children[path] = router.tree
        
    def get_handler(self, route, **kwargs) -> Node:
        node = self.tree.find(route, **kwargs)
        return node