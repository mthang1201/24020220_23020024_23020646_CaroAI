import time
from functools import wraps

class Timer:
    """A context manager and decorator to measure execution time."""
    def __init__(self, name="Execution"):
        self.name = name
        self.start_time = None
        self.end_time = None
        self.duration = 0.0

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time

def time_it(func):
    """Decorator to print execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[{func.__name__}] Execution time: {(end - start):.4f} seconds")
        return result
    return wrapper
