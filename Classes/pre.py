import re

class PreOps:

    @staticmethod
    def filter(code):
        return re.sub(r"(#=)((.|[\r\n])*?)(=#)", "", code)