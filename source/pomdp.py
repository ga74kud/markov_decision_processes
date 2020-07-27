from source.mdp import *



class pomdp(mdp):
    def __init__(self, **kwargs):
        self.po_dict={'O': None}
        super().__init__()

