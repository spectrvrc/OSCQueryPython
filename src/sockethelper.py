import socket 
from random import randint
from typing import Literal

def find_available_port(protocol: Literal['udp', 'tcp']) -> int:
    found = False
    tries = 0
    while not found:
        port = randint(10001, 65535)
        try:
            if tries > 1000:
                break
            if protocol == 'udp':
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.bind(("", port))
                    s.close()
                    found = True
            else:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(("", port))
                    s.close()
                    found = True
        except:
            tries += 1
            continue
        
    raise Exception(f"Could not find available `{protocol}` port.")