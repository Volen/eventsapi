from deta import Deta

def get_deta():
    # remove secret key before deploy
    deta = Deta("c0b313oq_QuVjFdj29QPY5mrfyi9QVwF49B4g1Syu")
    return deta