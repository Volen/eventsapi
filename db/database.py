import os
from deta import Deta

def get_deta():    
    deta = Deta(os.environ['DETA_API'])
    return deta