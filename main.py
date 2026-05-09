import socket

def is_host_alive(ip: str, port: int = 80, timeout: float = 1.0) -> bool:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(timeout)
    
    result = s.connect_ex((ip,port))
        
    s.close()
    return result == 0

print(is_host_alive("8.8.8.8"))        # harusnya True
print(is_host_alive("192.168.99.99"))  # harusnya False
