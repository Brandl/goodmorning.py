mods = {}

def add_mod(func):
    mods[func.__name__] = func
    return func

@add_mod
def requests(attr):
   print('request',attr)

@add_mod
def jsonpath(attr):
   print('jsonpath',attr)

@add_mod
def template(attr):
   print('template',attr)


"""
@add_mod
def epson-pos:
    from escpos.printer import Network
    thermal=Network("192.168.0.4")
    thermal.text("Hello World\n")
    thermal.cut()
"""
