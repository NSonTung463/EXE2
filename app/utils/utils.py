import datetime

def get_current_time() -> str:
    '''
    Get the current time in the string format.
    '''
    return datetime.datetime.now().isoformat()