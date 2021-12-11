from requests_cache import CachedSession
from datetime import timedelta
from jsonpath_ng.ext import parse
from jinja2 import Environment, BaseLoader


blocks = {}

def add_block(func):
    blocks[func.__name__] = func
    return func

@add_block
def requests(method: str, url: str, headers: list, flow={}):
    session = CachedSession('req_cache', expire_after=3600, backend='sqlite')
    response = session.request(method, url, headers=headers)
    return response.json()

@add_block
def jsonpath(paths: list, flow={}):
    result = {}

    for path in paths:
        # get querys from list TODO: might be simple if dict instead
        name, query = list(path.items())[0]
        jsonpath_expr = parse(query)
        matches = jsonpath_expr.find(flow['prev'])
        
        # Single match
        if len(matches) == 1:
            result.update({name: str(matches[0].value)})
        # Make liste from multi matches
        elif len(matches) > 1:
            match_list = []
            for match in matches:
                match_list.append(match.value)
            result.update({name: match_list})
    return result

@add_block
def template(text:str, flow={}):
    print(text, flow['prev'])
    template = Environment(loader=BaseLoader()).from_string(text)
    return template.render(**flow['prev'])

@add_block
def epsonpos(ip:str, flow={}):
    from escpos.printer import Network
    thermal=Network(ip)
    thermal.text(flow['text'])
    thermal.cut()

@add_block
def console(flow={}):
    print(flow['text'])

