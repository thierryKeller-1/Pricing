import socket


def is_connexion_enabled(host='8.8.8.8', port=53, timeout=10) -> bool:
    try:
        sock = socket.create_connection((host, port), timeout)
        sock.close()
        return True
    except (socket.timeout, OSError):
        return False
    
def is_in_rotation() -> bool:
    return True