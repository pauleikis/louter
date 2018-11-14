from contextlib import contextmanager


@contextmanager
def trace(text):
    print(text + ' START')
    yield
    print(text + ' END')
