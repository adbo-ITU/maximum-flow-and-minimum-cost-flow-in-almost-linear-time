import os

ENABLE_LOG = 'ENABLE_LOG' in os.environ

def log(*args, **kwargs):
    if ENABLE_LOG:
        print(*args, **kwargs)
