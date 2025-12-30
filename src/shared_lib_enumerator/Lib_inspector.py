import subprocess
import re

class Lib_inspector:
    def __init__(self):
        self.version = "1.0.0"

    def inspect(self, lib_path, sieve_ = True):
        result = subprocess.check_output(["nm", "-D", "--defined-only", lib_path]).decode()
        funcs = []
        
        pattern = re.compile(r'[0-9a-fA-F]+\s+[TW]\s+([a-zA-Z_][a-zA-Z0-9_]*)')

        for line in result.splitlines():
            match = pattern.search(line)
            if match:
                func_name = match.group(1)
                
                if not sieve_ or not func_name.startswith('_'):
                    funcs.append(func_name)
        
        return sorted(funcs)
    
_instance = Lib_inspector()