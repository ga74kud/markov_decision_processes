from source.usecases.uc_pomdp.mdp import *



class pomdp_class(mdp):
    def __init__(self, **kwargs):
        self.po_dict={'O': None}
        super().__init__()

