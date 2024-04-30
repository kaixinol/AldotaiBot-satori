from importlib import import_module


def loader(lst: list[str]):
    for _ in lst:
        import_module(_)
