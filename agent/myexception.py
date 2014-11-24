class MyExcept(Exception):
        def __init__(self, str="Caught a custom Exception"):
                self.errormsg = str
        def __repr__(self):
                return self.errormsg
