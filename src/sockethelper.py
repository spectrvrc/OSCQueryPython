import socket 
from random import randint
from typing import Literal

def find_available_port(protocol: Literal['udp', 'tcp', 'both'], preferred: int) -> int:
    found = False
    tries = 0
    port = preferred
    while not found:
        try:
            if tries > 1000:
                break
            if protocol == 'udp':
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.bind(("", port))
                    s.close()
                    return port
            elif protocol == 'tcp':
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(("", port))
                    s.close()
                    return port
            elif protocol == 'both':
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.bind(("", port))
                    s.close()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(("", port))
                    s.close()
                return port
            else:
                raise Exception(f"Unknown protocol `{protocol}`")
        except:
            tries += 1
            port = randint(10001, 65535)
            continue

    raise Exception(f"Could not find available `{protocol}` port.")