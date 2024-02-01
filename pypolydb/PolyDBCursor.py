
from .utilities import *

class PolyDBCursor() :

    def __init__(self,cur):
        self._cursor = cur

    def next(self):
        try:
            return self._cursor.next()
        except StopIteration:
            return False

    def __iter__(self):
        return self
    
    def __next__(self):
            return _sanitize_result(self._cursor.next())