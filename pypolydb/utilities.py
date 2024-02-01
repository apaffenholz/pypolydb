
__all__ = ['_sanitize_result']

def _sanitize_result(obj : dict) -> dict:
    if isinstance(obj, dict):
        if '_attrs' in obj:
            del obj['_attrs'] 
        if '_polyDB' in obj:
            del obj['_polyDB'] 
        if '_type' in obj:
            del obj['_type'] 
        if '_ns' in obj:
            del obj['_ns'] 
    
    return obj
    