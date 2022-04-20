from deta import Deta

def get_deta():    
    deta = Deta(ENV['DETA_API'])
    return deta