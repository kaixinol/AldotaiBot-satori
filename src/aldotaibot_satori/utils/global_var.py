var = {}


def get_var():
    global var
    return var


def set_var(key, value):
    global var
    var[key] = value
