
__all__ = ['_sanitize_result']

def _sanitize_result(obj : dict) -> dict:
    if isinstance(obj, dict):
        if '_attrs' in obj:
            del obj['_attrs'] 
    
    return obj
    